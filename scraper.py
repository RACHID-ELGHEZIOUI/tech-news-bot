import requests
from bs4 import BeautifulSoup
from typing import List, Dict

def get_news() -> List[Dict[str, str]]:
    news_list = []
    url = "https://news.ycombinator.com/"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    
    for item in soup.select(".athing")[:10]:
        title_elem = item.select_one(".titleline > a")
        if title_elem:
            news_list.append({
                "title": title_elem.text,
                "link": title_elem.get("href"),
                "source": "Hacker News"
            })
    return news_list