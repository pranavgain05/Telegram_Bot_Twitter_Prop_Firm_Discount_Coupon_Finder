import asyncio
import aiohttp
from bs4 import BeautifulSoup

BOT_TOKEN = "8715379481:AAH3DDvgE_53hGuO3ZgMbFfk-DdXLnZt2zM"
CHAT_ID = "7179654594"

SEARCHES = [
    "prop firm discount",
    "prop firm coupon",
    "funded account giveaway",
    "100% discount prop firm",
    "prop firm challenge free",
    "trading challenge coupon",
    "funded account code",
    "100% discount coupon"
]

sent = set()

async def send(session, msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    await session.post(url, data={"chat_id": CHAT_ID, "text": msg})

async def fetch(session, url):
    try:
        async with session.get(url, headers={"User-Agent": "Mozilla/5.0"}) as res:
            return await res.text()
    except:
        return ""

async def scan_query(session, query):
    url = f"https://nitter.net/search?f=tweets&q={query.replace(' ', '+')}"
    html = await fetch(session, url)

    soup = BeautifulSoup(html, "html.parser")
    tweets = soup.find_all("div", class_="timeline-item")

    for t in tweets[:10]:
        text_tag = t.find("div", class_="tweet-content")
        link_tag = t.find("a", class_="tweet-link")

        if text_tag and link_tag:
            text = text_tag.get_text().strip()
            link = "https://twitter.com" + link_tag["href"]

            key = text[:100]

            if key not in sent:
                msg = f"🚨 NEW PROP FIRM POST\n\n{text[:200]}\n\n🔗 {link}"
                await send(session, msg)
                sent.add(key)

async def main():
    async with aiohttp.ClientSession() as session:
        await send(session, "✅ Bot started - scanning posts...")

        while True:
            tasks = []
            for query in SEARCHES:
                tasks.append(scan_query(session, query))

            await asyncio.gather(*tasks)
            await asyncio.sleep(10)

asyncio.run(main())
