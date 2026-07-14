const axios = require('axios');
const Tender = require('../models/Tender');

const scrape_gem_tenders = async (maxPages = 5) => {
  try {
    console.log('Loading GEM bids page...');
    const pageResp = await axios.get('https://bidplus.gem.gov.in/all-bids');
    const html = pageResp.data;

    const match = html.match(/id="chash"\s+type="hidden"\s+value="([^"]+)"/);
    if (!match) {
      console.log('Could not find CSRF token');
      return 0;
    }

    const csrfToken = match[1];
    console.log(`CSRF token: ${csrfToken.substring(0, 20)}...`);

    let count = 0;

    for (let pageNum = 1; pageNum <= maxPages; pageNum++) {
      console.log(`\nFetching page ${pageNum}...`);

      const payload = {
        page: pageNum,
        param: { searchBid: '', searchType: 'fullText' },
        filter: {
          bidStatusType: 'ongoing_bids',
          byType: 'all',
          highBidValue: '',
          byEndDate: { from: '', to: '' },
          sort: 'Bid-End-Date-Latest'
        }
      };

      try {
        const resp = await axios.post('https://bidplus.gem.gov.in/all-bids-data',
          `payload=${encodeURIComponent(JSON.stringify(payload))}&csrf_bd_gem_nk=${csrfToken}`,
          { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
        );

        const docs = resp.data?.response?.response?.docs || [];
        if (!docs.length) {
          console.log(`No more tenders on page ${pageNum}. Stopping.`);
          break;
        }

        for (const doc of docs) {
          try {
            const extractStr = (val, defaultVal = 'N/A') => {
              if (Array.isArray(val)) return val.length ? val[0] : defaultVal;
              return val ? String(val) : defaultVal;
            };

            let title = extractStr(doc.bbt_title);
            if (title === 'N/A') title = extractStr(doc.b_category_name);

            const ministry = extractStr(doc.ba_official_details_minName, '');
            const dept = extractStr(doc.ba_official_details_deptName, '');
            const department = (ministry && dept) ? `${ministry} - ${dept}` : ministry || dept || 'N/A';

            const bidId = extractStr(doc.b_id, '');
            const bidNumber = extractStr(doc.b_bid_number, '');
            const link = `https://bidplus.gem.gov.in/showbidDocument/${bidId}`;

            const existing = await Tender.findOne({ reference_link: link });
            if (existing) continue;

            const category = extractStr(doc.b_category_name, 'General');

            await Tender.create({
              title,
              department,
              closing_date: extractStr(doc.final_end_date_sort),
              published_date: extractStr(doc.final_start_date_sort),
              tender_value: 'N/A',
              reference_link: link,
              summary: `Bid: ${bidNumber} | ${title}`,
              location: 'India',
              source: 'gem',
              category,
              state: 'All India'
            });

            count++;
            console.log(`Saved: ${title.substring(0, 60)}...`);
          } catch (err) {
            if (err.code === 11000) continue;
            console.log(`Error parsing bid: ${err.message}`);
          }
        }
      } catch (err) {
        console.log(`Error fetching page ${pageNum}: ${err.message}`);
        break;
      }

      await new Promise(r => setTimeout(r, 1000));
    }

    console.log(`\nTotal GEM tenders saved: ${count}`);
    return count;
  } catch (err) {
    console.error('GEM scraper error:', err.message);
    return 0;
  }
};

module.exports = { scrape_gem_tenders };
