const express = require('express');
const router = express.Router();
const { scrape_gem_tenders } = require('../services/gemScraper');

router.post('/gem', async (req, res) => {
  scrape_gem_tenders().catch(err => console.error('Background scrape error:', err.message));
  res.json({ message: 'GEM scrape started in background' });
});

module.exports = router;
