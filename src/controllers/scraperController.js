const { scrape_gem_tenders } = require('../services/gemScraper');

const scrapeGEM = async (req, res) => {
  scrape_gem_tenders().catch(err => console.error('Background scrape error:', err.message));
  res.json({ message: 'GEM scrape started in background' });
};

module.exports = { scrapeGEM };
