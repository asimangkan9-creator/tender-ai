const Tender = require('../models/Tender');
const { get_ai_recommendation } = require('../services/ai');

const searchTenders = async (req, res) => {
  try {
    const { keyword, location, source } = req.body;

    const query = {
      $or: [
        { title: { $regex: keyword, $options: 'i' } },
        { department: { $regex: keyword, $options: 'i' } },
        { summary: { $regex: keyword, $options: 'i' } }
      ]
    };

    if (location) query.location = { $regex: location, $options: 'i' };
    if (source) query.source = source;

    const tenders = await Tender.find(query);

    if (!tenders.length) {
      return res.json({ ai_answer: 'No tenders found.', results: [] });
    }

    const ai_answer = await get_ai_recommendation(keyword || '', tenders);
    res.json({ ai_answer, results: tenders });
  } catch (err) {
    res.json({ ai_answer: `Error: ${err.message}`, results: [] });
  }
};

module.exports = { searchTenders };
