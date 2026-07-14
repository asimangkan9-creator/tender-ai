const mongoose = require('mongoose');

const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017';
const MONGO_DB = process.env.MONGO_DB || 'tender_ai';

const connectDB = async () => {
  try {
    await mongoose.connect(MONGO_URI, {
      dbName: MONGO_DB,
      serverSelectionTimeoutMS: 5000
    });
    console.log('MongoDB connected');
  } catch (err) {
    console.error('MongoDB connection error:', err.message);
    console.log('Retrying in 10 seconds...');
    setTimeout(connectDB, 10000);
  }
};

module.exports = connectDB;
