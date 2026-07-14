const express = require('express');
const router = express.Router();
const { createTender, getTenders, getTenderById, updateTender, deleteTender } = require('../controllers/tenderController');

router.post('/', createTender);
router.get('/', getTenders);
router.get('/:id', getTenderById);
router.put('/:id', updateTender);
router.delete('/:id', deleteTender);

module.exports = router;
