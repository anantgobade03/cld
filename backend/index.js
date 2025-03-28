const express = require('express');
const axios = require('axios');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());

// Geocoding endpoint
app.get('/api/geocode', async (req, res) => {
  try {
    const response = await axios.get(`https://api.opencagedata.com/geocode/v1/json?q=${req.query.city}&key=${req.query.apiKey}`);
    const { lat, lng } = response.data.results[0].geometry;
    res.json({ lat, lng });
  } catch (error) {
    res.status(500).json({ error: 'Geocoding failed' });
  }
});

// Weather endpoint
app.get('/api/weather', async (req, res) => {
  try {
    // Implement OpenWeatherMap API call here
    res.json({
      rainfall_24h: 50,
      rainfall_72h: 120,
      temperature: 25
    });
  } catch (error) {
    res.status(500).json({ error: 'Weather fetch failed' });
  }
});

// Prediction endpoint
app.post('/api/predict', async (req, res) => {
  try {
    // Implement your model prediction logic here
    res.json({ probability: 0.65 });
  } catch (error) {
    res.status(500).json({ error: 'Prediction failed' });
  }
});

app.listen(5000, () => console.log('Backend running on port 5000'));