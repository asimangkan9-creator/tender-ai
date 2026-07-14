import httpx
import re
from crud import create_tender, get_tender_by_reference_link
from models import TenderCreate


async def scrape_gem_tenders(max_pages: int = 5):
    """Scrape GEM tenders from bidplus.gem.gov.in via AJAX API."""
    async with httpx.AsyncClient() as client:
        print("Loading GEM bids page...")
        resp = await client.get("https://bidplus.gem.gov.in/all-bids")

        match = re.search(r'id="chash"\s+type="hidden"\s+value="([^"]+)"', resp.text)
        if not match:
            print("Could not find CSRF token")
            return 0

        csrf_token = match.group(1)
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
                resp = await client.post(
                    "https://bidplus.gem.gov.in/all-bids-data",
                    data={"payload": str(payload), "csrf_bd_gem_nk": csrf_token}
                )
                data = resp.json()
                docs = data.get("response", {}).get("response", {}).get("docs", [])

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

                        existing = await get_tender_by_reference_link(link)
                        if existing:
                            continue

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

        print(f"\nTotal GEM tenders saved: {count}")
        return count


if __name__ == "__main__":
    import asyncio
    asyncio.run(scrape_gem_tenders())