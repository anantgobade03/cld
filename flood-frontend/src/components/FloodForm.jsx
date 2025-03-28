// import { Chart } from 'chart.js/auto';
// import { useEffect, useRef } from 'react';
// import { FiAlertTriangle } from 'react-icons/fi';

import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default marker icons
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon-2x.png',
  iconUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-icon.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.7.1/dist/images/marker-shadow.png',
});

import { useState } from "react";
import axios from "axios";

const FloodForm = () => {
  const [formData, setFormData] = useState({
    city: "",
    date: "",
    soilMoisture: "",
    riverLevel: "",
    reservoirLevel: "",
    previousFloods: "",
  });

  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    try {
      const response = await axios.post("http://127.0.0.1:5000/predict", formData);
      setData(response.data);
    } catch (err) {
      setError("Error fetching data. Please check inputs and try again.");
    } finally {
      setIsLoading(false);
    }
  };

  // Add this helper function above your component
  const getCircleColor = (probability) => {
    if (probability < 35) return '#4CAF50';  // Green
    if (probability >= 35 && probability <= 70) return '#FF9800';  // Orange
    return '#F44336';  // Red
  };

  // const chartRef = useRef(null);

  // useEffect(() => {
  //   if (data && chartRef.current) {
  //     const ctx = chartRef.current.getContext('2d');
  //     new Chart(ctx, {
  //       type: 'line',
  //       data: {
  //         labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Current'],
  //         datasets: [{
  //           label: 'Flood Probability (%)',
  //           data: [15, 22, 35, 28, 42, data.flood_probability],
  //           borderColor: '#3498db',
  //           backgroundColor: 'rgba(52, 152, 219, 0.1)',
  //           fill: true,
  //           tension: 0.4
  //         }]
  //       },
  //       options: {
  //         responsive: true,
  //         scales: {
  //           y: {
  //             beginAtZero: true,
  //             max: 100
  //           }
  //         }
  //       }
  //     });
  //   }
  // }, [data]);

  return (
    <div className="flood-form-container">
      <h2 className="form-title">Flood Prediction System</h2>
      <form onSubmit={handleSubmit} className="prediction-form">
        <div className="form-group">
          <label htmlFor="city">City Name</label>
          <input
            type="text"
            id="city"
            name="city"
            placeholder="Enter city name"
            value={formData.city}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="date">Date</label>
          <input
            type="date"
            id="date"
            name="date"
            value={formData.date}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="soilMoisture">Soil Moisture (%)</label>
          <input
            type="number"
            id="soilMoisture"
            name="soilMoisture"
            placeholder="0-100%"
            min="0"
            max="100"
            value={formData.soilMoisture}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="riverLevel">River Level (meters)</label>
          <input
            type="number"
            id="riverLevel"
            name="riverLevel"
            placeholder="River height in meters"
            step="0.01"
            min="0"
            value={formData.riverLevel}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="reservoirLevel">Reservoir Level (%)</label>
          <input
            type="number"
            id="reservoirLevel"
            name="reservoirLevel"
            placeholder="0-100%"
            min="0"
            max="100"
            value={formData.reservoirLevel}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="previousFloods">Previous Floods (last month)</label>
          <input
            type="number"
            id="previousFloods"
            name="previousFloods"
            placeholder="Number of floods in last month"
            min="0"
            value={formData.previousFloods}
            onChange={handleChange}
            required
          />
        </div>

        <button type="submit" disabled={isLoading} className="submit-btn">
          {isLoading ? "Processing..." : "Get Flood Prediction"}
        </button>
      </form>

      {error && <div className="error-message">{error}</div>}

      {data && (
        <div className="results-container">
          <h3 className="results-title">Prediction Results</h3>
          
          <div className="weather-info">
            <h4>Weather Information</h4>
            <div className="info-grid">
              <div>
                <span className="info-label">24h Rainfall:</span>
                <span className="info-value">{data.rainfall_24h} mm</span>
              </div>
              <div>
                <span className="info-label">72h Rainfall:</span>
                <span className="info-value">{data.rainfall_72h} mm</span>
              </div>
              <div>
                <span className="info-label">Temperature:</span>
                <span className="info-value">{data.temperature} °C</span>
              </div>
              <div>
                <span className="info-label">Coordinates:</span>
                <span className="info-value">{data.latitude}, {data.longitude}</span>
              </div>
            </div>
          </div>

          <div className="prediction-info">
            <h4>Flood Prediction</h4>
            <div className={`prediction-result ${data.flood_prediction ? 'flood-risk' : 'no-flood-risk'}`}>
              {data.flood_prediction ? "HIGH FLOOD RISK" : "LOW FLOOD RISK"} 
              <span className="probability">({data.flood_probability}% probability)</span>
            </div>
          </div>

          <div className="risk-visualization">
            <h4>Risk Level</h4>
            <div className="risk-indicator">
              <div 
                className="risk-marker" 
                style={{ left: `${data.flood_probability}%` }}
              />
            </div>
            <div className="risk-labels">
              <span>Low</span>
              <span>Medium</span>
              <span>High</span>
            </div>
          </div>

          <div className="map-container" style={{ margin: '20px 0', height: '400px' }}>
            <h3>Flood Risk Map</h3>
            <MapContainer 
              center={[data.latitude, data.longitude]} 
              zoom={12} 
              style={{ height: '100%' }}
            >
              <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
              <Marker position={[data.latitude, data.longitude]}>
                <Popup>
                  <div className="map-popup">
                    <h4>{formData.city}</h4>
                    <div className="popup-details">
                      <p><strong>Flood Risk:</strong> {data.flood_prediction ? "High" : "Low"}</p>
                      <p><strong>Probability:</strong> {data.flood_probability}%</p>
                      <p><strong>24h Rainfall:</strong> {data.rainfall_24h} mm</p>
                      <p><strong>River Level:</strong> {data.river_level} m</p>
                    </div>
                  </div>
                </Popup>
              </Marker>
              <Circle
                center={[data.latitude, data.longitude]}
                radius={2000}
                color={getCircleColor(data.flood_probability)}
                fillColor={getCircleColor(data.flood_probability)}
                fillOpacity={0.2}
                weight={2}
              />
            </MapContainer>
          </div>

          {/* <div className="chart-container">
            <h4>Historical Trend</h4>
            <canvas ref={chartRef}></canvas>
          </div> */}

          <div className="input-summary">
            <h4>Your Input Summary</h4>
            <div className="info-grid">
              <div>
                <span className="info-label">Soil Moisture:</span>
                <span className="info-value">{data.soil_moisture}%</span>
              </div>
              <div>
                <span className="info-label">River Level:</span>
                <span className="info-value">{data.river_level} m</span>
              </div>
              <div>
                <span className="info-label">Reservoir Level:</span>
                <span className="info-value">{data.reservoir_level}%</span>
              </div>
              <div>
                <span className="info-label">Previous Floods:</span>
                <span className="info-value">{data.previous_floods}</span>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default FloodForm;