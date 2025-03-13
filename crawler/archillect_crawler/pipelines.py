import os
import hashlib
import requests
import psycopg2
import torch
import torchvision.transforms as transforms
from PIL import Image
from io import BytesIO
import numpy as np
from skimage.color import rgb2lab
from torchvision import models

class NIMA:
    """
    A simplified NIMA (Neural Image Assessment) implementation using a pre-trained ResNet
    modified to predict aesthetic scores.
    """
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = models.resnet50(pretrained=True)
        # Modify the last layer to output a single score
        num_ftrs = self.model.fc.in_features
        self.model.fc = torch.nn.Sequential(
            torch.nn.Linear(num_ftrs, 256),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.5),
            torch.nn.Linear(256, 1),
            torch.nn.Sigmoid()  # Normalize output between 0 and 1
        )
        self.model = self.model.to(self.device)
        self.model.eval()
        
        # Image preprocessing
        self.transform = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

    def predict(self, img):
        """
        Predict aesthetic score for an image.
        Returns a score between 0 and 10.
        """
        with torch.no_grad():
            img_tensor = self.transform(img).unsqueeze(0).to(self.device)
            score = self.model(img_tensor).item()
            # Convert score from [0,1] to [1,10] range
            return score * 9 + 1

class NIMAPipeline:
    def __init__(self):
        self.model = None
        self.conn = None
        self.useDb = True

    def open_spider(self, spider):
        # Load DB connection info from environment
        if self.useDb:
            self.db_host = os.environ.get("DB_HOST", "localhost")
            self.db_port = os.environ.get("DB_PORT", "5432")
            self.db_name = os.environ.get("DB_NAME", "archillect")
            self.db_user = os.environ.get("DB_USER", "postgres")
            self.db_pass = os.environ.get("DB_PASS", "password")

            # # Connect to DB
            self.conn = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_pass
            )
        
            # Create table if it doesn't exist
            cur = self.conn.cursor()
            create_table_query = """
            CREATE TABLE IF NOT EXISTS images (
                id SERIAL PRIMARY KEY,
                url VARCHAR(255) NOT NULL,
                source_url TEXT NOT NULL,
                caption TEXT,
                timestamp TIMESTAMP DEFAULT NOW(),
                score FLOAT NOT NULL,
                hash VARCHAR(32) UNIQUE
            );
            """
            cur.execute(create_table_query)
            self.conn.commit()
            cur.close()

        # # Initialize NIMA model
        self.model = NIMA()

    def close_spider(self, spider):
        if self.conn:
            self.conn.close()

    def process_item(self, item, spider):
        image_url = item["image_url"]

        # Download image
        try:
            r = requests.get(image_url, timeout=10)
            if r.status_code != 200:
                raise Exception(f"Failed to download image: {r.status_code}")
        except Exception as e:
            spider.logger.error(f"Error downloading {image_url}: {e}")
            return None

        image_data = r.content

        # Calculate MD5 hash for deduplication
        md5_hash = hashlib.md5(image_data).hexdigest()
        
        # Check if image already exists
        if self.useDb and self.is_duplicate(md5_hash):
            spider.logger.info(f"Duplicate image found: {image_url}")
            return None

        # Open and validate image
        try:
            img = Image.open(BytesIO(image_data)).convert("RGB")
            width, height = img.size
            
            # Skip very small images
            if width < 256 or height < 256:
                spider.logger.info(f"Image too small: {width}x{height}")
                return None
                
            # Skip images with extreme aspect ratios
            aspect_ratio = width / height
            if aspect_ratio < 0.5 or aspect_ratio > 2.0:
                spider.logger.info(f"Extreme aspect ratio: {aspect_ratio}")
                return None
                
        except Exception as e:
            spider.logger.error(f"Error processing image {image_url}: {e}")
            return None

        # Score image with NIMA
        try:
            score = self.model.predict(img)
            
            # Skip low-scoring images
            if score < 5.0:
                spider.logger.info(f"Low aesthetic score: {score}")
                return None
                
        except Exception as e:
            spider.logger.error(f"Error scoring image {image_url}: {e}")
            return None

        # Save image locally
        os.makedirs("images", exist_ok=True)
        filename = f"images/{md5_hash}.jpg"
        try:
            with open(filename, "wb") as f:
                f.write(image_data)
        except Exception as e:
            spider.logger.error(f"Error saving image {filename}: {e}")
            return None

        # Insert into database
        if self.useDb:
            insert_query = """
            INSERT INTO images (url, source_url, caption, score, hash)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id;
            """
            try:
                with self.conn.cursor() as cur:
                    cur.execute(insert_query, (
                        f"/images/{md5_hash}.jpg",
                        item["source_url"],
                        item["caption"],
                        score,
                        md5_hash
                    ))
                    self.conn.commit()
            except Exception as e:
                spider.logger.error(f"Database error: {e}")
                return None

        # Update item with additional info
        item["hash"] = md5_hash
        item["score"] = score
        item["url"] = f"/images/{md5_hash}.jpg"
        return item

    def is_duplicate(self, md5_hash):
        """Check if an image with this hash already exists."""
        with self.conn.cursor() as cur:
            cur.execute("SELECT 1 FROM images WHERE hash = %s", (md5_hash,))
            return cur.fetchone() is not None 