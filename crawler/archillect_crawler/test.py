from scrapy.linkextractors import LinkExtractor
import re

rule2_regex = r'tumblr\.com/.+/post/\d+'
tag_page_url = "https://www.tumblr.com/tagged/aesthetic%20images"
post_page_url = "https://www.tumblr.com/whispers-of-the-night/775251181601718272" # <--- REPLACE WITH YOUR POST URL

print(f"Testing regex: {rule2_regex}")
print("\n--- Testing against TAG PAGE URL ---")
if re.search(rule2_regex, tag_page_url):
    print(f"REGEX MATCHES TAGs PAGE URL: {tag_page_url} (Unexpected)")
else:
    print(f"REGEX DOES NOT MATCH TAG PAGE URL: {tag_page_url} (Expected)")

print("\n--- Testing against POST PAGE URL ---")
if re.search(rule2_regex, post_page_url):
    print(f"REGEX MATCHES POST PAGE URL: {post_page_url} (Expected)")
else:
    print(f"REGEX DOES NOT MATCH POST PAGE URL: {post_page_url} (Unexpected)")

# --- Optional: Test LinkExtractor directly (though regex test is usually enough) ---
print("\n--- Testing LinkExtractor directly on response (Tag Page) ---")
le_rule2 = LinkExtractor(allow=(rule2_regex,))
links_rule2 = le_rule2.extract_links(response) # 'response' is from the tag page
print(f"Links extracted by Rule 2 LinkExtractor from TAG PAGE: {links_rule2}") # Should ideally be empty or very few, from tag page itself, not from posts listed.