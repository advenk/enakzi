import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from archillect_crawler.items import ArchillectItem  # Assuming your items.py is in archillect_crawler
import re

class GeneralSpider(CrawlSpider):
    name = "general"

    start_urls = [
        "https://www.tumblr.com/whispers-of-the-night",
        "https://www.tumblr.com/tagged/aesthetic%20images",
        "https://www.behance.net/galleries",
        "https://www.artstation.com/?sort_by=community&dimension=all",
        "https://unsplash.com/",
        "https://www.reddit.com/r/Art/top/?t=month",
        "https://www.reddit.com/r/DigitalArt/top/?t=month",
        "https://www.reddit.com/r/SpecArt/top/?t=month",
    ]

    allowed_domains = [
        'tumblr.com',
        'behance.net',
        'artstation.com',
        'deviantart.com',
        'unsplash.com',
        'reddit.com',
        'redd.it',  # Reddit's image domain
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow=(), # Rule 1: Keep broad follow rule for now
                deny=(
                    r'\.(pdf|zip|rar|exe)$',
                    r'/search/',
                    r'/settings/',
                    r'/account/',
                )
            ),
            follow=True
        ),
        Rule(
            LinkExtractor(
                allow=(
                    # r'tumblr\.com\/.+\/(\d+)$'  # Rule 2: Refined regex to match post URLs ending in digits
                ),
            ),
            callback='parse_item',
            follow=True
        ),
    )

    def parse_item(self, response):
        print(f"parse_item called for: {response.url}")  # DEBUG: Check if parse_item is called

        for img in response.css('img'):
            # Get the image URL from data-src or src
            image_url = img.attrib.get('data-src') or img.attrib.get('src')

            # Ensure an image URL exists
            if image_url and not re.search(r'(thumb|icon|avatar|logo)', image_url, re.I):
                print(f"Found image URL: {image_url}")

                if re.search(r'a\d+\.behance\.net\/.*?\/footer\/', image_url, re.I) and image_url.endswith('.webp'):
                    print(f"Skipping banner URL: {image_url}") # Optional logging
                    continue  # Skip to the next image if it's a banner
                # Clean up the URL
                image_url = response.urljoin(image_url)

                

                # Build item
                item = ArchillectItem()
                item["image_url"] = image_url
                item["source_url"] = response.url
                print(f"Item: {item}")

                # Get caption from various possible sources
                caption = (
                    img.attrib.get('alt') or
                    img.attrib.get('title') or
                    response.css('h1::text').get() or
                    response.css('title::text').get() or
                    ""
                ).strip()
                print(f"Caption: {caption}")
                item["caption"] = caption
                yield item