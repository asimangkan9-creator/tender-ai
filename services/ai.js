const axios = require('axios');

const OLLAMA_URL = process.env.OLLAMA_URL || 'http://localhost:11434';
const OLLAMA_MODEL = process.env.OLLAMA_MODEL || 'llama3.2';

const get_ai_recommendation = async (query, tenders) => {
  try {
    const top10 = tenders.slice(0, 10);
    const tenderList = top10.map((t, i) =>
      `${i + 1}. Title: ${t.title} | Dept: ${t.department} | Closes: ${t.closing_date || 'N/A'} | Value: ${t.tender_value || 'N/A'}`
    ).join('\n');

    const prompt = `You are a government tender advisor. Based on these tenders:\n\n${tenderList}\n\nUser query: "${query}"\n\nProvide a brief recommendation of which tenders are most relevant and why.`;

    const response = await axios.post(`${OLLAMA_URL}/api/generate`, {
      model: OLLAMA_MODEL,
      prompt,
      stream: false
    }, { timeout: 60000 });

    return response.data.response || 'No recommendation available.';
  } catch (err) {
    return `AI recommendation unavailable. Found ${tenders.length} matching tenders.`;
  }
};

const chat_with_ai = async (message) => {
  try {
    const response = await axios.post(`${OLLAMA_URL}/api/generate`, {
      model: OLLAMA_MODEL,
      prompt: message,
      stream: false
    }, { timeout: 60000 });

    return response.data.response || 'No response from AI.';
  } catch (err) {
    return 'AI service is currently unavailable. Please try again later.';
  }
};

module.exports = { get_ai_recommendation, chat_with_ai };
