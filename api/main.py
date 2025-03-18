import os
import sys
import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the config
from config.config import DB_CONFIG, API_CONFIG

app = FastAPI(title="expl0rer API")

# Allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static images
app.mount("/images", StaticFiles(directory=API_CONFIG["images_dir"]), name="images")

# Database connection parameters
DB_HOST = DB_CONFIG["host"]
DB_PORT = DB_CONFIG["port"]
DB_NAME = DB_CONFIG["dbname"]
DB_USER = DB_CONFIG["user"]
DB_PASS = DB_CONFIG["password"]

class Image(BaseModel):
    id: int
    url: str
    source_url: str
    caption: Optional[str]
    timestamp: datetime
    score: float
    hash: str

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

@app.get("/")
def read_root():
    return {"message": "Welcome to expl0rer API"}

@app.get("/images", response_model=List[Image])
def get_images(
    limit: int = 20,
    offset: int = 0,
    min_score: Optional[float] = None,
    sort_by: str = "score",  # Can be 'score', 'timestamp'
    order: str = "desc"      # Can be 'asc', 'desc'
):
    """
    Get a paginated list of images with optional filtering and sorting.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    # Build the query
    query = "SELECT id, url, source_url, caption, timestamp, score, hash FROM images"
    params = []

    # Add score filter if specified
    if min_score is not None:
        query += " WHERE score >= %s"
        params.append(min_score)

    # Add sorting
    if sort_by not in ["score", "timestamp"]:
        sort_by = "score"
    if order not in ["asc", "desc"]:
        order = "desc"
    
    query += f" ORDER BY {sort_by} {order}"

    # Add pagination
    query += " LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    try:
        cur.execute(query, params)
        rows = cur.fetchall()
        
        images = []
        for row in rows:
            images.append(Image(
                id=row[0],
                url=row[1],
                source_url=row[2],
                caption=row[3],
                timestamp=row[4],
                score=row[5],
                hash=row[6]
            ))
        
        return images
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.get("/images/{image_id}", response_model=Image)
def get_image(image_id: int):
    """
    Get a single image by its ID.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT id, url, source_url, caption, timestamp, score, hash
            FROM images WHERE id = %s
        """, (image_id,))
        
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Image not found")
            
        return Image(
            id=row[0],
            url=row[1],
            source_url=row[2],
            caption=row[3],
            timestamp=row[4],
            score=row[5],
            hash=row[6]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.get("/stats")
def get_stats():
    """
    Get statistics about the image collection.
    """
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        stats = {}
        
        # Total images
        cur.execute("SELECT COUNT(*) FROM images")
        stats["total_images"] = cur.fetchone()[0]
        
        # Average score
        cur.execute("SELECT AVG(score) FROM images")
        stats["average_score"] = round(cur.fetchone()[0] or 0, 2)
        
        # Score distribution
        cur.execute("""
            SELECT 
                COUNT(*) FILTER (WHERE score >= 9) as excellent,
                COUNT(*) FILTER (WHERE score >= 7 AND score < 9) as good,
                COUNT(*) FILTER (WHERE score >= 5 AND score < 7) as average
            FROM images
        """)
        dist = cur.fetchone()
        stats["score_distribution"] = {
            "excellent": dist[0],
            "good": dist[1],
            "average": dist[2]
        }
        
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close() 