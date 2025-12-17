import feedparser
from datetime import datetime
from typing import List, Tuple
from feedparser import FeedParserDict

RSS_FEEDS = {
    'Risky Business': "http://risky.biz/feeds/risky-business-news/",
    'ESPN': "https://www.espn.com/espn/rss/news",
    'HNRSS': "https://hnrss.org/frontpage",
    'The Hacker News': 'https://feeds.feedburner.com/TheHackersNews',
    'thaddeus grugq newsletter': 'https://buttondown.com/grugq/rss',
    'SANS Daily': "https://isc.sans.edu/dailypodcast.xml",
    'SANS Education': "https://isc.sans.edu/rssfeed.xml",
    'Microsoft Blog': "https://msrc.microsoft.com/blog/categories/security-research-defense/feed",
    'Seclists': "https://seclists.org/rss/fulldisclosure.rss",
    'Darknet Diaries': "https://www.darknet.org.uk/feed/",
    'Krebs on Security': "https://krebsonsecurity.com/feed/",
    'Security Magazine': "https://www.securitymagazine.com/rss/15",
    'CVE Feed': 'https://cvefeed.io/rssfeed/newsroom.xml',
    'CISA News': "https://www.cisa.gov/news.xml",
    'CISA Blog': "https://www.cisa.gov/blog.xml",
    'Cyberscoop': 'https://cyberscoop.com/feed/',
    'tl;dr': 'https://rss.beehiiv.com/feeds/xgTKUmMmUm.xml',
    '404 Media': 'https://www.404media.co/rss/',
    'Cyber Security Headlines': 'https://cisoseries.libsyn.com/rss',
    'CISA Cyber Advisory': "https://www.cisa.gov/cybersecurity-advisories/all.xml",
    'NY Times': "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml",
    "NPR News": "https://feeds.npr.org/1001/rss.xml",
    'NPR Technology': "https://feeds.npr.org/1019/rss.xml",
    "Simplecast": "https://feeds.simplecast.com/54nAGcIl",
    "The Record": "https://therecord.media/tag/rss",
    "Ars Technica": "https://feeds.arstechnica.com/arstechnica/index",
    "TedTalks": "http://feeds.feedburner.com/TEDTalks_video",
    "r/technology": "https://www.reddit.com/r/technology/.rss",
    "BBC News": "http://feeds.bbci.co.uk/news/world/rss.xml",
    "New Heights": "https://rss.art19.com/new-heights",
    "Politico": "https://www.politico.com/rss/politicopicks.xml",
    "Politico Cybersecurity": "https://rss.politico.com/morningcybersecurity.xml",
    "CISO Series": 'https://cisoseries.libsyn.com/rss',
    'CS Hub': 'https://www.cshub.com/rss/articles',
    'Mens College Basketball': 'https://www.ncaa.com/news/basketball-men/d1/rss.xml',
    'FBS Football': 'https://www.ncaa.com/news/football/fbs/rss.xml',
    'Graham Cluey': 'https://grahamcluley.com/feed/'
}

SITE_TITLE = 'RSS News Aggregator'
OUTPUT_HTML_FILE = 'index.html'
MAX_ITEMS=5 # gets the first 5 entries for each RSS

# Function to get the RSS Feeds
def get_rss_feeds(RSS_FEEDS: dict) -> list[tuple[str, dict]]: 
    feeds = []
    # loops to find the name and url from the RSS feeds
    for name, url in RSS_FEEDS.items():
        # if successful
        try:
            # parses the url
            feed = feedparser.parse(url)
            # appends the name and feed
            feeds.append((name, feed))
        except Exception as e:
            # if not successful
            print(f"Error parsing {url}: {e}")
    return feeds

# Function that generates the HTML and CSS for the website
def html_generator(feeds: list[tuple[str, dict]]) -> str:
    head = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset=UTF-8>
        <title>{SITE_TITLE}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                padding: 20px;
            }}
            .container {{
                max-width: 900px;
                margin: auto;
                background: white;
                padding: 20px;
                border-radius: 10px;
            }}
            .entry {{
                border-bottom: 1px solid #ddd;
                margin-bottom: 20px;
                padding-bottom: 10px;
            }}
            .entry h2 {{
                margin: 0 0 10px;
            }}
            .entry a {{
                text-decoration: none;
                color: #333;
            }}
            .entry a:hover {{
                color: #0077cc;
            }}
            .date {{
                color: #888;
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{SITE_TITLE}</h1>
            <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    """
    body_parts = []
    # loops through the RSS feeds
    for feed_name, feed in feeds:
        section = [f"<h2>{feed_name}</h2>"]
        # loop that gets first 5 entires for each
        for entry in feed.entries[:MAX_ITEMS]:
            # gets the title
            title = entry.get("title", "No Title")
            # gets the link
            link = entry.get("link", "#")
            # gets the published date
            published = entry.get("published", "No Date")
            # CSS code that generates the HTML
            section.append(f"""
                <div class='entry'>
                    <h2><a href='{link}'>{title}</a></h2>
                    <p class='date'>{published}</p>
                </div>
            """)
        # appends the section
        body_parts.append('\n'.join(section))

    footer = """
        </div>
    </body>
</html>
    """
    # joins the HTML code
    html_body = '\n'.join(body_parts) if body_parts else "<p>No entries found.</p>"
    # returns the HTML
    return f"{head}{html_body}{footer}"

# function to save the HTML file
def save_html(content: str, filename: str) -> None:
    try:
        # write the content to the file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"HTML file generated: {filename}")
    except IOError as e:
        print(f"Error saving HTML file: {e}")

def main():
    try:
        # get the RSS Feeds
        feeds = get_rss_feeds(RSS_FEEDS)
        # generate the HTML
        html_content = html_generator(feeds)
        # save the HTML
        save_html(html_content, OUTPUT_HTML_FILE)
    except IOError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()