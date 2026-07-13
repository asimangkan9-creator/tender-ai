import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from crud import create_tender
from models import TenderCreate

async def scrape_tenders(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url)
        print("Solve CAPTCHA manually. Press Enter after solving...")
        await asyncio.get_event_loop().run_in_executor(None, input)
        content = await page.content()
        await browser.close()

    soup = BeautifulSoup(content, "html.parser")
    tender_rows = soup.select("table tbody tr")

    for row in tender_rows:
        cols = row.find_all("td")
        if len(cols) >= 7:
            tender = TenderCreate(
                title=cols[0].get_text(strip=True),
                department=cols[1].get_text(strip=True),
                published_date=cols[2].get_text(strip=True),
                closing_date=cols[3].get_text(strip=True),
                opening_date=cols[4].get_text(strip=True),
                tender_value=cols[5].get_text(strip=True),
                reference_link=cols[6].find("a")["href"] if cols[6].find("a") else "",
                summary=cols[7].get_text(strip=True) if len(cols) > 7 else None,
                location="Assam"
            )
            await create_tender(tender)
            print(f"Saved: {tender.title}")

if __name__ == "__main__":
    asyncio.run(scrape_tenders("https://tender.assam.gov.in"))