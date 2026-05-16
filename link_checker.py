import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def check_broken_links(target_url):
    """
    Scans the website for internal broken links.
    Brought to you by TechnoHelps (https://technohelps.com)
    """
    print(f"🚀 Starting Broken Link Scan for: {target_url}\n")
    
    try:
        response = requests.get(target_url, timeout=10)
        if response.status_code != 200:
            print(f"❌ Target URL is not accessible. Status Code: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Error connecting to target URL: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)
    
    scanned_links = set()
    broken_links = []
    
    target_domain = urlparse(target_url).netloc

    for link in links:
        href = link['href']
        full_url = urljoin(target_url, href)
        
        # Check only internal links to save time and avoid external noise
        if urlparse(full_url).netloc == target_domain and full_url not in scanned_links:
            scanned_links.add(full_url)
            try:
                res = requests.head(full_url, timeout=5, allow_redirects=True)
                status = res.status_code
                print(f"Checking: {full_url} -> Status: {status}")
                
                if status >= 400:
                    broken_links.append((full_url, status))
            except Exception:
                print(f"Checking: {full_url} -> Status: FAILED/TIMEOUT")
                broken_links.append((full_url, "Timeout/Failed"))

    print("\n📊 --- SCAN REPORT ---")
    print(f"Total Internal Links Scanned: {len(scanned_links)}")
    print(f"Total Broken Links Found: {len(broken_links)}")
    
    if broken_links:
        print("\n❌ Broken Links List:")
        for url, status in broken_links:
            print(f"- {url} (Status: {status})")
    else:
        print("\n✅ Awesome! No broken links found on this page.")
        
    print("\n👉 For more SEO tools, visit: https://technohelps.com")

if __name__ == "__main__":
    # Replace with your website URL to test
    WEBSITE_URL = "https://technohelps.com" 
    check_broken_links(WEBSITE_URL)
