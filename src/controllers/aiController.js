const { chat_with_ai } = require('../services/ai');

const chat = async (req, res) => {
  try {
    const message = req.body.message || req.query.message || '';
    const response = await chat_with_ai(message);
    res.json({ response });
  } catch (err) {
    res.json({ response: 'Error: ' + err.message });
  }
};

module.exports = { chat };
