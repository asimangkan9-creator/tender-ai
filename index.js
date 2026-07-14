require('dotenv').config();
const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
const connectDB = require('./src/config/db');
const tendersRouter = require('./src/routes/tenders');
const searchRouter = require('./src/routes/search');
const scraperRouter = require('./src/routes/scraper');
const { chat } = require('./src/controllers/aiController');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

connectDB();

app.get('/', (req, res) => {
  res.json({ message: 'Tender Search AI API' });
});

app.get('/debug', (req, res) => {
  const uri = process.env.MONGO_URI || 'NOT SET';
  const maskedUri = uri.replace(/\/\/[^:]+:[^@]+@/, '//***:***@');
  const mongooseState = mongoose.connection.readyState;
  const states = ['disconnected', 'connected', 'connecting', 'disconnecting'];
  res.json({
    mongoUri: maskedUri,
    mongoDb: process.env.MONGO_DB || 'NOT SET',
    mongooseState: states[mongooseState] || 'unknown'
  });
});

app.use('/tenders', tendersRouter);
app.use('/search', searchRouter);
app.use('/scrape', scraperRouter);

app.post('/chat', chat);

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
