import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from crud import create_tender
from models import TenderCreate


async def scrape_gem_tenders(url: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url)

        print("Login or solve CAPTCHA if needed. Press Enter after the page loads fully...")
        await asyncio.get_event_loop().run_in_executor(None, input)

        content = await page.content()
        await browser.close()

    soup = BeautifulSoup(content, "html.parser")
    tender_cards = soup.select(".bid-card, .tender-item, .card, [class*=bid], [class*=tender]")

    if not tender_cards:
        tender_cards = soup.select("table tbody tr")

    count = 0
    for card in tender_cards:
        try:
            title = card.select_one("h5, h4, h3, .title, [class*=title], td:nth-child(2)")
            department = card.select_one(".dept, .department, [class*=dept], td:nth-child(3)")
            closing = card.select_one(".date, .closing, [class*=close], td:nth-child(4)")
            value = card.select_one(".value, .amount, [class*=value], td:nth-child(5)")
            link = card.select_one("a[href]")

            title_text = title.get_text(strip=True) if title else "N/A"
            dept_text = department.get_text(strip=True) if department else "N/A"
            closing_text = closing.get_text(strip=True) if closing else "N/A"
            value_text = value.get_text(strip=True) if value else "N/A"
            link_href = link["href"] if link and link.has_attr("href") else ""
            if link_href and not link_href.startswith("http"):
                link_href = "https://gem.gov.in" + link_href

            tender = TenderCreate(
                title=title_text,
                department=dept_text,
                closing_date=closing_text,
                tender_value=value_text,
                reference_link=link_href,
                summary=title_text,
                location="India",
                source="gem",
                category="Government",
                state="All India"
            )
            await create_tender(tender)
            count += 1
            print(f"Saved: {tender.title}")
        except Exception as e:
            print(f"Error parsing card: {e}")
            continue

    print(f"\nTotal tenders saved: {count}")


if __name__ == "__main__":
    asyncio.run(scrape_gem_tenders("https://gem.gov.in/bids"))