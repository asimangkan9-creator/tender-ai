const mongoose = require('mongoose');

const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017';
const MONGO_DB = process.env.MONGO_DB || 'tender_ai';

const connectDB = async () => {
  try {
    const maskedUri = MONGO_URI ? MONGO_URI.replace(/\/\/[^:]+:[^@]+@/, '//***:***@') : 'NOT SET';
    console.log('Connecting to:', maskedUri);
    console.log('DB name:', MONGO_DB);
    await mongoose.connect(MONGO_URI, {
      dbName: MONGO_DB,
      serverSelectionTimeoutMS: 15000,
      connectTimeoutMS: 15000,
      tls: true,
      tlsAllowInvalidCertificates: true
    });
    console.log('MongoDB connected');
  } catch (err) {
    console.error('MongoDB connection error:', err.message);
    console.log('Retrying in 15 seconds...');
    setTimeout(connectDB, 15000);
  }
};

module.exports = connectDB;
