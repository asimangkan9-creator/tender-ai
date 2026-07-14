require('dotenv').config();
const express = require('express');
const cors = require('cors');
const connectDB = require('./config/db');
const tendersRouter = require('./routes/tenders');
const searchRouter = require('./routes/search');
const scraperRouter = require('./routes/scraper');
const { chat_with_ai } = require('./services/ai');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

connectDB();

app.get('/', (req, res) => {
  res.json({ message: 'Tender Search AI API' });
});

app.use('/tenders', tendersRouter);
app.use('/search', searchRouter);
app.use('/scrape', scraperRouter);

app.post('/chat', async (req, res) => {
  try {
    const message = req.body.message || req.query.message || '';
    const response = await chat_with_ai(message);
    res.json({ response });
  } catch (err) {
    res.json({ response: 'Error: ' + err.message });
  }
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
