import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const API_BASE = 'http://localhost:8000';

const states = ['Chhattisgarh', 'Maharashtra', 'Punjab'];
const districts = ['Raipur', 'Nagpur', 'Ludhiana', 'Amravati', 'Patiala'];

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('recommendation');
  const [state, setState] = useState('Maharashtra');
  const [district, setDistrict] = useState('Nagpur');
  const [data, setData] = useState({ rec: [], profit: [], yield: [], ranking: [], weather: {}, mandi: {} });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchData = async (tab) => {
    setLoading(true);
    setError('');
    try {
      const promises = {
        rec: axios.get(`${API_BASE}/recommendation/?state=${state}&district=${district}`),
        profit: axios.get(`${API_BASE}/profit/${state}`),
        yield: axios.get(`${API_BASE}/yield/${state}`),
        ranking: axios.get(`${API_BASE}/ranking/${state}`),
        weather: axios.get(`${API_BASE}/weather/${state}`),
      };
      const results = await Promise.all(Object.values(promises));
      setData({
        rec: results[0].data,
        profit: results[1].data,
        yield: results[2].data,
        ranking: results[3].data,
        weather: results[4].data,
      });
    } catch (err) {
      setError(err.message);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchData(activeTab);
  }, [state, district]);

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

  return (
    <div className="dashboard">
      <header>
        <h1>CROP DECISION SUPPORT SYSTEM</h1>
        <p>Hydrology &amp; Agriculture Analytics</p>
      </header>

      <div className="controls">
        <select value={state} onChange={(e) => setState(e.target.value)}>
          {states.map(s => <option key={s}>{s}</option>)}
        </select>
        <select value={district} onChange={(e) => setDistrict(e.target.value)}>
          {districts.map(d => <option key={d}>{d}</option>)}
        </select>
        <button onClick={() => fetchData(activeTab)} disabled={loading}>
          {loading ? 'Loading...' : 'Refresh'}
        </button>
      </div>

      {error &amp;&amp; <div className="error">Error: {error}</div>}

      <div className="tabs">
        {['recommendation', 'profit', 'yield', 'ranking', 'mandi', 'weather'].map(tab => (
          <button key={tab} className={activeTab === tab ? 'active' : ''} onClick={() => setActiveTab(tab)}>
            {tab.charAt(0).toUpperCase() + tab.slice(1).replace('_', ' ')}
          </button>
        ))}
      </div>

      <div className="content">
        {activeTab === 'recommendation' &amp;&amp; (
          <div>
            <h2>Top Recommended Crops</h2>
            <div className="cards">
              {data.rec.map((item, i) => (
                <div key={i} className="card">
                  <h3>{item.crop}</h3>
                  <p>Predicted Yield: {item.predicted_yield?.toFixed(1)}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'profit' &amp;&amp; (
          <div>
            <h2>Profit Forecast</h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={data.profit}>
                <CartesianGrid />
                <XAxis dataKey="crop" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="expected_profit" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {activeTab === 'yield' &amp;&amp; (
          <div>
            <h2>Yield Predictions</h2>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie data={data.yield.slice(0,5)} dataKey="predicted_yield" nameKey="crop" cx="50%" cy="50%" outerRadius={80}>
                  {data.yield.slice(0,5).map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}

        {activeTab === 'ranking' &amp;&amp; (
          <div>
            <h2>Crop Ranking</h2>
            <ul>
              {data.ranking.map((item, i) => (
                <li key={i}>{item.crop}: ₹{item.expected_revenue?.toLocaleString() || 0}</li>
              ))}
            </ul>
          </div>
        )}

        {activeTab === 'mandi' &amp;&amp; (
          <div>
            <h2>Mandi Prices</h2>
            <p>Select crop for forecast (add input)</p>
            <p>Demo: Groundnut Forecast: ₹{data.mandi.forecast_price || 'N/A'}</p>
          </div>
        )}

        {activeTab === 'weather' &amp;&amp; (
          <div>
            <h2>Weather Summary</h2>
            <p>Avg Temp: {data.weather.avg_temp?.toFixed(1)}°C</p>
            <p>Avg Rainfall: {data.weather.avg_rainfall?.toFixed(1)}mm</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;

