const mongoose = require('mongoose');

const MONGO_URI = process.env.MONGO_URI || 'mongodb://localhost:27017';
const MONGO_DB = process.env.MONGO_DB || 'tender_ai';

const connectDB = async () => {
  try {
    const maskedUri = MONGO_URI ? MONGO_URI.replace(/\/\/[^:]+:[^@]+@/, '//***:***@') : 'NOT SET';
    console.log('Connecting to:', maskedUri);
    console.log('DB name:', MONGO_DB);

    const opts = {
      dbName: MONGO_DB,
      serverSelectionTimeoutMS: 15000,
      connectTimeoutMS: 15000
    };

    if (!MONGO_URI.includes('tls=')) {
      opts.tls = true;
      opts.tlsAllowInvalidCertificates = true;
    }

    await mongoose.connect(MONGO_URI, opts);
    console.log('MongoDB connected successfully');
  } catch (err) {
    console.error('MongoDB connection error:', err.message);
    console.error('Full error:', JSON.stringify(err, null, 2));
    console.log('Retrying in 15 seconds...');
    setTimeout(connectDB, 15000);
  }
};

mongoose.connection.on('error', (err) => {
  console.error('Mongoose error event:', err.message);
});

mongoose.connection.on('disconnected', () => {
  console.log('Mongoose disconnected');
});

module.exports = connectDB;
