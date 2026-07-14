const express = require('express');
const router = express.Router();
const { scrapeGEM } = require('../controllers/scraperController');

router.post('/gem', scrapeGEM);

module.exports = router;
