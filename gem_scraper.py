import asyncio
from playwright.async_api import async_playwright
from crud import create_tender
from models import TenderCreate


async def scrape_gem_tenders(max_pages: int = 5):
    """Scrape GEM tenders from bidplus.gem.gov.in via AJAX API."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        print("Loading GEM bids page...")
        await page.goto("https://bidplus.gem.gov.in/all-bids", wait_until="networkidle")
        await page.wait_for_selector("#chash", state="attached", timeout=30000)

        csrf_token = await page.evaluate("document.getElementById('chash').value")
        print(f"CSRF token: {csrf_token[:20]}...")

        count = 0
        for page_num in range(1, max_pages + 1):
            print(f"\nFetching page {page_num}...")

            payload = {
                "page": page_num,
                "param": {"searchBid": "", "searchType": "fullText"},
                "filter": {
                    "bidStatusType": "ongoing_bids",
                    "byType": "all",
                    "highBidValue": "",
                    "byEndDate": {"from": "", "to": ""},
                    "sort": "Bid-End-Date-Latest"
                }
            }

            try:
                csrf = csrf_token
                response = await page.evaluate("""
                    async ([payload, csrf]) => {
                        const formData = new FormData();
                        formData.append('payload', JSON.stringify(payload));
                        formData.append('csrf_bd_gem_nk', csrf);
                        const res = await fetch('/all-bids-data', {method: 'POST', body: formData});
                        return await res.json();
                    }
                """, [payload, csrf])

                docs = response.get("response", {}).get("response", {}).get("docs", [])
                if not docs:
                    print(f"No more tenders on page {page_num}. Stopping.")
                    break

                for doc in docs:
                    try:
                        def extract_str(val, default="N/A"):
                            if isinstance(val, list):
                                return val[0] if val else default
                            return str(val) if val else default

                        title = extract_str(doc.get("bbt_title", ""))
                        if title == "N/A":
                            title = extract_str(doc.get("b_category_name", ["N/A"]))

                        ministry = extract_str(doc.get("ba_official_details_minName", ""), "")
                        dept = extract_str(doc.get("ba_official_details_deptName", ""), "")
                        department = f"{ministry} - {dept}" if ministry and dept else ministry or dept or "N/A"

                        bid_id = extract_str(doc.get("b_id", ""), "")
                        bid_number = extract_str(doc.get("b_bid_number", ""), "")

                        link = f"https://bidplus.gem.gov.in/showbidDocument/{bid_id}"

                        tender = TenderCreate(
                            title=title,
                            department=department,
                            closing_date=extract_str(doc.get("final_end_date_sort", "")),
                            published_date=extract_str(doc.get("final_start_date_sort", "")),
                            tender_value="N/A",
                            reference_link=link,
                            summary=f"Bid: {bid_number} | {title}",
                            location="India",
                            source="gem",
                            category=extract_str(doc.get("b_category_name", ["General"])),
                            state="All India"
                        )
                        await create_tender(tender)
                        count += 1
                        print(f"Saved: {tender.title[:60]}...")
                    except Exception as e:
                        print(f"Error parsing bid: {e}")
                        continue

            except Exception as e:
                print(f"Error fetching page {page_num}: {e}")
                break

            await asyncio.sleep(1)

        await browser.close()
        print(f"\nTotal GEM tenders saved: {count}")
        return count


if __name__ == "__main__":
    asyncio.run(scrape_gem_tenders())
