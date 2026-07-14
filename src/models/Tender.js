const mongoose = require('mongoose');

const tenderSchema = new mongoose.Schema({
  title:          { type: String, required: true },
  department:     { type: String, required: true },
  published_date: { type: String, default: null },
  closing_date:   { type: String, default: null },
  opening_date:   { type: String, default: null },
  tender_value:   { type: String, default: null },
  reference_link: { type: String, required: true, unique: true },
  summary:        { type: String, default: null },
  location:       { type: String, default: null },
  source:         { type: String, default: 'assam' },
  category:       { type: String, default: null },
  state:          { type: String, default: null },
  scraped_at:     { type: Date, default: Date.now }
});

tenderSchema.index({ title: 1 });
tenderSchema.index({ department: 1 });
tenderSchema.index({ closing_date: 1 });

module.exports = mongoose.model('Tender', tenderSchema);
