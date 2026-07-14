const express = require('express');
const router = express.Router();
const Tender = require('../models/Tender');

router.post('/', async (req, res) => {
  try {
    const tender = await Tender.create(req.body);
    res.status(201).json(tender);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});

router.get('/', async (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 100;
    const tenders = await Tender.find().limit(limit);
    res.json(tenders);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.get('/:id', async (req, res) => {
  try {
    const tender = await Tender.findById(req.params.id);
    if (!tender) return res.status(404).json({ error: 'Tender not found' });
    res.json(tender);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.put('/:id', async (req, res) => {
  try {
    const tender = await Tender.findByIdAndUpdate(req.params.id, req.body, { new: true });
    if (!tender) return res.status(404).json({ error: 'Tender not found' });
    res.json(tender);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.delete('/:id', async (req, res) => {
  try {
    const tender = await Tender.findByIdAndDelete(req.params.id);
    if (!tender) return res.status(404).json({ error: 'Tender not found' });
    res.json({ message: 'Tender deleted' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;
