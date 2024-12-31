import requests
import re
from bs4 import BeautifulSoup
from time import sleep

def fetch_sitemap_urls(sitemap_url):
    """Fetch URLs from the sitemap."""
    try:
        response = requests.get(sitemap_url, headers={ 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36' })
        response.raise_for_status()  # Check for HTTP request errors
        # soup = BeautifulSoup(response.content, 'xml')
        
        # Regular expression to capture the `href` attribute inside the <xhtml:link> tag
        pattern = r'<xhtml:link.*?rel="alternate".*?href="(.*?)".*?>'

        # Extract all matches
        urls_temp = re.findall(pattern, response.content.decode("utf-8"))

        unique_urls = []
        for url in urls_temp:
            if '/en/' not in url and url not in unique_urls:
                unique_urls.append(url)

        # Remove duplicates by converting the list to a set, then back to a list (if order matters, use sorted)
        urls = list(set(unique_urls))

        for url in urls:
            print(url)

        return urls
    except Exception as e:
        print(f"Error fetching sitemap: {e}")
        return []

def visit_urls(urls):
    """Visit each URL to trigger TranslatePress."""
    for i, url in enumerate(urls, 1):
        try:
            print(f"[{i}/{len(urls)}] Visiting: {url}")
            response = requests.get(url)
            
            # Check for successful request
            if response.status_code == 200:
                print(f"✅ Successfully visited {url}")
            else:
                print(f"⚠️ Failed to visit {url} (Status Code: {response.status_code})")
            
            # Sleep to avoid overloading the server
            sleep(15)  # Adjust delay as needed
        except Exception as e:
            print(f"Error visiting {url}: {e}")

if __name__ == "__main__":
    # The sitemap URL
    sitemap_url = "https://journal.singularwm.com/post-sitemap.xml"
    
    print("Fetching URLs from the sitemap...")
    urls = fetch_sitemap_urls(sitemap_url)
    
    if urls:
        print(f"Found {len(urls)} URLs. Starting to visit...")
        visit_urls(urls)
    else:
        print("No URLs found in the sitemap.")
