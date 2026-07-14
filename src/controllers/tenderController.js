const Tender = require('../models/Tender');

const createTender = async (req, res) => {
  try {
    const tender = await Tender.create(req.body);
    res.status(201).json(tender);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
};

const getTenders = async (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 100;
    const tenders = await Tender.find().limit(limit);
    res.json(tenders);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

const getTenderById = async (req, res) => {
  try {
    const tender = await Tender.findById(req.params.id);
    if (!tender) return res.status(404).json({ error: 'Tender not found' });
    res.json(tender);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

const updateTender = async (req, res) => {
  try {
    const tender = await Tender.findByIdAndUpdate(req.params.id, req.body, { new: true });
    if (!tender) return res.status(404).json({ error: 'Tender not found' });
    res.json(tender);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

const deleteTender = async (req, res) => {
  try {
    const tender = await Tender.findByIdAndDelete(req.params.id);
    if (!tender) return res.status(404).json({ error: 'Tender not found' });
    res.json({ message: 'Tender deleted' });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
};

module.exports = { createTender, getTenders, getTenderById, updateTender, deleteTender };
