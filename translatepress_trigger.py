import requests
from bs4 import BeautifulSoup
from time import sleep

def fetch_sitemap_urls(sitemap_url):
    """Fetch URLs from the sitemap."""
    try:
        # Fetch the HTML content of the sitemap
        response = requests.get(sitemap_url)
        response.raise_for_status()  # Raise HTTPError for bad responses

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Locate the table with URLs
        table = soup.find('table', {'id': 'sitemap'})
        if not table:
            raise ValueError("No table with id 'sitemap' found in the HTML.")

        # Extract all URLs from <a> tags within the table
        urls = []
        for a_tag in table.find_all('a', href=True):
            urls.append(a_tag['href'])

        return urls
    except requests.exceptions.RequestException as e:
        print(f"Error fetching sitemap: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
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
            sleep(10)  # Adjust delay as needed
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
