import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from explorer_crawler.items import ExplorerItem
import re

class GeneralSpider(CrawlSpider):
    name = "general"

    start_urls = [
        # "https://www.tumblr.com/communities/browse/art",
        # "https://www.behance.net/galleries",
        # "https://www.artstation.com/?sort_by=community&dimension=all",
        # "https://unsplash.com/",
        # "https://www.reddit.com/r/Art/top/?t=month",
        # "https://www.reddit.com/r/DigitalArt/top/?t=month",
        # "https://www.reddit.com/r/SpecArt/top/?t=month",
        # "https://www.flickr.com/photos/tags",
        # "https://dribbble.com/shots/popular",
        # "https://www.thisiscolossal.com/"
        # "https://www.juxtapoz.com/",
        "https://archillect.com/",
        # "https://www.booooooom.com/"
        # "https://www.pinterest.com/ideas/art/961238559656/",
        # "https://www.pinterest.com/ideas/design/902065567321/"
    ]

    allowed_domains = [
        'tumblr.com',
        'behance.net',
        'artstation.com',
        'deviantart.com',
        'unsplash.com',
        'reddit.com',
        'redd.it',
        "flickr.com",
        "pinterest.com",
        "thisiscolossal.com",
        "juxtapoz.com",
        "booooooom.com",
        "archillect.com"
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow=(),  # Explore all links broadly
                deny=(
                    r'\.(pdf|zip|rar|exe)$',  # Skip files
                    r'/search/',
                    r'/settings/',
                    r'/account/',
                    r'/login/',
                    r'/signup/',
                    r'/forgot/',
                    r'/reset/',
                    r'/verify/',
                    r'/confirm/',
                    r'/verify-email/',
                )
            ),
            follow=True,  # Keep following links
            callback='parse_for_images'  # Check every page for images
        ),
    )

    def parse_for_images(self, response):
        """
        Check if the page has an image. If it does, treat it as a leaf page,
        scrape it, and stop following links from here. If not, let the crawl continue.
        """
        print(f"Checking page: {response.url}")

        # Look for images on the page
        for img in response.css('img'):
            image_url = img.attrib.get('data-src') or img.attrib.get('src')

            # Ensure an image URL exists and isn’t a thumbnail/icon/banner
            if (image_url and
                not re.search(r'(thumb|icon|avatar|logo)', image_url, re.I) and  # Skip thumbnails/icons
                re.search(r'\.(jpg|jpeg|png|webp)$', image_url, re.I) and       # Only allow raster images
                not image_url.endswith('.svg')): 
                print(f"Found image URL: {image_url}")

                # Skip unwanted banner images (e.g., Behance footers)
                if re.search(r'a\d+\.behance\.net\/.*?\/footer\/', image_url, re.I) and image_url.endswith('.webp'):
                    print(f"Skipping banner URL: {image_url}")
                    continue

                # Clean up the URL
                image_url = response.urljoin(image_url)

                # Build item
                item = ExplorerItem()
                item["image_url"] = image_url
                item["source_url"] = response.url

                # Get caption from various possible sources
                caption = (
                    img.attrib.get('alt') or
                    img.attrib.get('title') or
                    response.css('h1::text').get() or
                    response.css('title::text').get() or
                    ""
                ).strip()
                item["caption"] = caption

                print(f"Leaf page found with image: {image_url}")
                yield item

                # Since we found an image, treat this as a leaf page and stop following links
                return  # Exit the function to prevent further link extraction

        # If no valid image is found, let the crawler keep following links via the rule
        print(f"No valid image found on {response.url}, continuing crawl...")