# scraper.py
import aiohttp
import asyncio
from bs4 import BeautifulSoup

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()

def is_relevant_link(link, keywords):
    href = link['href']
    text = link.get_text()
    return any(keyword in href or keyword in text for keyword in keywords)

async def scrape_website(url, depth=1, keywords=None):
    if depth < 1:
        return {}

    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        soup = BeautifulSoup(html, 'html.parser')

        data = {
            'url': url,
            'title': soup.title.string if soup.title else '',
            'content': soup.get_text(),
            'links': []
        }

        links = soup.find_all('a', href=True)
        for link in links:
            if keywords and not is_relevant_link(link, keywords):
                continue
            href = link['href']
            if href.startswith('http'):
                data['links'].append(href)

        nested_data = []
        if depth > 1:
            tasks = [scrape_website(link, depth - 1, keywords) for link in data['links']]
            nested_data = await asyncio.gather(*tasks)

        data['nested_links'] = nested_data

        return data
