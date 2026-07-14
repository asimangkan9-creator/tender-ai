const express = require('express');
const router = express.Router();
const { searchTenders } = require('../controllers/searchController');

router.post('/', searchTenders);

module.exports = router;
