from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


class Website:
    def __init__(self, url: str, name: str = ""):
        self.url = url
        self.name = name

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        self.title = soup.title.string if soup.title else "No title found"

        if soup.body:
            # remove noisy tags before extracting text
            for irrelevant in soup.body(["script", "style", "img", "input"]):
                irrelevant.decompose()
            text = soup.body.get_text(separator="\n", strip=True)
        else:
            text = ""

        # equivalent to fetch_website_contents(url)
        self.contents = (self.title + "\n\n" + text)[:2_000]

        # equivalent to fetch_website_links(url)
        self.links = [
            urljoin(self.url, link.get("href")) for link in soup.find_all("a") if link.get("href")
        ]
