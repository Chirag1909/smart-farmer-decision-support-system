import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from 'recharts';

const API_BASE = 'http://localhost:8000';
const token = localStorage.getItem('token') ? `Bearer ${localStorage.getItem('token')}` : '';

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('recommendation');
  const [statesList, setStatesList] = useState(['Chhattisgarh', 'Maharashtra', 'Punjab']);
  const [state, setState] = useState('Maharashtra');
  const [district, setDistrict] = useState('Nagpur');
  const [data, setData] = useState({ rec: [], profit: [], yield: [], ranking: [], weather: {}, mandi: [] });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    axios.get(`${API_BASE}/states`, { headers: { Authorization: token } })
      .then(res => setStatesList(res.data.states))
      .catch(() => {});
  }, []);

  const fetchData = async () => {
    setLoading(true);
    setError('');
    try {
      const headers = { Authorization: token };
      const promises = {
        rec: axios.get(`${API_BASE}/recommendation/?state=${state}&district=${district}`, { headers }).catch(() => ({data: []})),
        profit: axios.get(`${API_BASE}/profit/${state}`, { headers }).catch(() => ({data: []})),
        yield: axios.get(`${API_BASE}/yield/${state}`, { headers }).catch(() => ({data: []})),
        ranking: axios.get(`${API_BASE}/ranking/${state}`, { headers }).catch(() => ({data: []})),
        weather: axios.get(`${API_BASE}/weather/${state}`, { headers }).catch(() => ({data: {}})),
        mandi: axios.get(`${API_BASE}/mandi/${state}`, { headers }).catch(() => ({data: []})),
      };
      const results = await Promise.all(Object.values(promises));
      setData({
        rec: results[0].data,
        profit: results[1].data,
        yield: results[2].data,
        ranking: results[3].data,
        weather: results[4].data,
        mandi: results[5].data,
      });
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  useEffect(() => {
    if (statesList.length) fetchData();
  }, [state]);

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d'];

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50 p-6">
      <div className="max-w-7xl mx-auto">
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent mb-4">
            🌾 Crop Decision Dashboard
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">AI-powered insights | Profit | Weather | Mandi | Ranking</p>
        </header>

        <div className="bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl p-8 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-end">
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-3">🌍 State</label>
              <select value={state} onChange={(e) => setState(e.target.value)} className="w-full p-4 border-2 border-gray-200 rounded-2xl focus:ring-4 focus:ring-green-200 transition-all shadow-sm hover:shadow-md">
                {statesList.map(s => <option key={s}>{s}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm font-bold text-gray-700 mb-3">🏘️ District</label>
              <input type="text" placeholder="e.g. Nagpur" value={district} onChange={(e) => setDistrict(e.target.value)} className="w-full p-4 border-2 border-gray-200 rounded-2xl focus:ring-4 focus:ring-blue-200 shadow-sm" />
            </div>
            <button onClick={fetchData} disabled={loading} className="bg-gradient-to-r from-green-600 to-emerald-600 text-white py-4 px-8 rounded-2xl font-bold text-lg shadow-lg hover:shadow-xl hover:from-green-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed">
              {loading ? '⟳ Loading...' : '✨ Get Recommendations'}
            </button>
          </div>
        </div>

        {error && <div className="bg-red-50 border border-red-200 text-red-800 p-4 rounded-2xl mb-8 text-center font-medium">{error}</div>}

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {['recommendation', 'profit', 'yield', 'ranking', 'mandi', 'weather'].map(tab => (
            <button
              key={tab}
              className={`p-6 rounded-3xl font-bold shadow-lg hover:shadow-2xl transition-all cursor-pointer border-2 ${
                activeTab === tab
                  ? 'bg-gradient-to-r from-green-500 to-emerald-600 text-white border-green-500 shadow-green-500/25'
                  : 'bg-white/50 backdrop-blur-sm text-gray-800 border-gray-200 hover:border-gray-400 hover:-translate-y-1'
              }`}
              onClick={() => setActiveTab(tab)}
            >
              <div className="text-3xl mb-2">
                {tab === 'recommendation' && '🏆'}
                {tab === 'profit' && '💰'}
                {tab === 'yield' && '📈'}
                {tab === 'ranking' && '🥇'}
                {tab === 'mandi' && '🏛️'}
                {tab === 'weather' && '☀️'}
              </div>
              <div>{tab.charAt(0).toUpperCase() + tab.slice(1).replace(/_/g, ' ')}</div>
            </button>
          ))}
        </div>

        <div className="space-y-8">
          {activeTab === 'recommendation' && (
            <div className="bg-white/70 backdrop-blur-xl p-8 rounded-3xl shadow-xl">
              <h2 className="text-4xl font-bold mb-8 bg-gradient-to-r from-green-600 to-teal-600 bg-clip-text text-transparent">🏆 Top Recommendations</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {data.rec.slice(0, 6).map((item, i) => (
                  <div key={i} className="group p-6 bg-gradient-to-b from-emerald-50 to-green-100 rounded-2xl border border-emerald-200 hover:shadow-2xl hover:-translate-y-2 transition-all">
                    <div className="flex items-start space-x-4">
                      <div className="w-12 h-12 bg-emerald-500 rounded-2xl flex items-center justify-center font-bold text-white text-xl group-hover:scale-110 transition">
                        #{i + 1}
                      </div>
                      <div className="flex-1">
                        <h3 className="text-2xl font-bold text-gray-900 mb-2">{item.crop}</h3>
                        <div className="space-y-1">
                          <p className="text-lg text-emerald-700 font-semibold">₹{(item.modal_price || 0).toLocaleString()}</p>
                          <p className="text-sm text-gray-600">Yield: {(item.predicted_yield || 0).toFixed(1)} kg/ha</p>
                          <p className="text-sm text-gray-600">Revenue: ₹{(item.expected_revenue || 0).toLocaleString()}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'profit' && (
            <div className="bg-white/70 backdrop-blur-xl p-8 rounded-3xl shadow-xl col-span-full">
              <h2 className="text-4xl font-bold mb-8 bg-gradient-to-r from-emerald-600 to-yellow-600 bg-clip-text text-transparent">💰 Profit Analysis</h2>
              <ResponsiveContainer width="100%" height={450}>
                <BarChart data={data.profit.slice(0, 10)}>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <XAxis dataKey="crop" angle={-45} height={90} tick={{ fontSize: 12 }} />
                  <YAxis />
                  <Tooltip formatter={(value) => [value.toLocaleString(), 'Profit ₹']} labelFormatter={(label) => `Crop: ${label}`} />
                  <Legend />
                  <Bar dataKey="expected_profit" fill="#10b981" name="Profit (₹)" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="profit_margin_%" fill="#f59e0b" name="Margin %" yAxisId="right" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          )}

          {activeTab === 'yield' && (
            <div className="bg-white/70 backdrop-blur-xl p-8 rounded-3xl shadow-xl col-span-full">
              <h2 className="text-4xl font-bold mb-8 bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">📈 Yield Predictions</h2>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <ResponsiveContainer width="100%" height={350}>
                  <PieChart>
                    <Pie data={data.yield.slice(0, 8)} dataKey="predicted_yield" nameKey="crop" cx="50%" cy="50%" outerRadius={100}>
                      {data.yield.slice(0, 8).map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
                <div className="space-y-4">
                  <h3 className="text-2xl font-bold text-gray-800">Top Yields</h3>
                  <ul className="space-y-2">
                    {data.yield.slice(0, 5).map((item, i) => (
                      <li key={i} className="flex items-center p-4 bg-gray-50 rounded-xl">
                        <span className="w-8 text-sm font-bold text-gray-500">{i + 1}.</span>
                        <span className="font-bold text-lg ml-3">{item.crop}</span>
                        <span className="ml-auto text-emerald-600 text-xl font-bold">{item.predicted_yield?.toFixed(1)} kg/ha</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'ranking' && (
            <div className="bg-white/70 backdrop-blur-xl p-8 rounded-3xl shadow-xl col-span-full">
              <h2 className="text-4xl font-bold mb-8 bg-gradient-to-r from-yellow-500 to-orange-500 bg-clip-text text-transparent">🥇 Mandi Ranking</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {data.ranking.slice(0, 10).map((item, i) => (
                  <div key={i} className="group p-6 bg-gradient-to-b from-yellow-50 to-orange-100 rounded-2xl border-l-4 border-yellow-400 hover:shadow-xl transition-all">
                    <div className="flex items-center mb-2">
                      <div className="w-12 h-12 bg-gradient-to-r from-yellow-400 to-orange-500 rounded-full flex items-center justify-center text-white font-bold text-xl shadow-lg mr-4 group-hover:scale-110 transition">
                        #{i + 1}
                      </div>
                      <h3 className="text-xl font-bold text-gray-900">{item.crop}</h3>
                    </div>
                    <div className="space-y-1 text-lg">
                      <p>Revenue: <span className="font-bold text-green-700">₹{item.expected_revenue?.toLocaleString()}</span></p>
                      <p>Yield: <span className="font-bold text-blue-600">{item.predicted_yield?.toFixed(1)} kg/ha</span></p>
                      <p>Price: <span className="font-bold text-orange-600">₹{item.modal_price?.toLocaleString()}</span></p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'mandi' && (
            <div className="bg-white/70 backdrop-blur-xl p-8 rounded-3xl shadow-xl col-span-full">
              <h2 className="text-4xl font-bold mb-8 bg-gradient-to-r from-orange-500 to-red-500 bg-clip-text text-transparent">🏛️ Live Mandi Prices</h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {data.mandi.slice(0, 9).map((item, i) => (
                  <div key={i} className="p-6 bg-gradient-to-br from-orange-50 to-red-100 rounded-2xl border border-orange-200 shadow-md hover:shadow-lg transition-all">
                    <h3 className="text-xl font-bold text-gray-900 mb-3">{item.crop || item.commodity}</h3>
                    <div className="text-3xl font-bold text-orange-600 mb-2">₹{item.modal_price?.toLocaleString()}</div>
                    <p className="text-sm text-gray-600 capitalize">{item.market}, {item.state}</p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {activeTab === 'weather' && (
            <div className="bg-white/70 backdrop-blur-xl p-8 rounded-3xl shadow-xl col-span-full">
              <h2 className="text-4xl font-bold mb-8 bg-gradient-to-r from-blue-500 to-cyan-500 bg-clip-text text-transparent">☀️ Weather & Climate</h2>
              {data.weather.error ? (
                <div className="text-center py-16 bg-gradient-to-r from-gray-50 to-gray-100 rounded-3xl">
                  <div className="text-6xl mb-4">🌤️</div>
                  <h3 className="text-2xl font-bold text-gray-600 mb-2">Weather Unavailable</h3>
                  <p className="text-gray-500">No data for {state}. Check connection or try another state.</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  <div className="bg-gradient-to-br from-blue-100 to-cyan-200 p-8 rounded-3xl text-center shadow-lg">
                    <div className="text-5xl mb-4">🌡️</div>
                    <h3 className="text-xl font-bold mb-2 text-gray-800">Temperature</h3>
                    <p className="text-4xl font-bold text-blue-700">{data.weather.temp || data.weather.avg_temp?.toFixed(1)}°C</p>
                  </div>
                  <div className="bg-gradient-to-br from-gray-100 to-slate-200 p-8 rounded-3xl text-center shadow-lg">
                    <div className="text-5xl mb-4">💧</div>
                    <h3 className="text-xl font-bold mb-2 text-gray-800">Humidity</h3>
                    <p className="text-4xl font-bold text-slate-700">{data.weather.humidity ? data.weather.humidity.toFixed(0) + '%' : 'N/A'}</p>
                  </div>
                  <div className="bg-gradient-to-br from-yellow-100 to-orange-200 p-8 rounded-3xl text-center shadow-lg">
                    <div className="text-5xl mb-4">🌬️</div>
                    <h3 className="text-xl font-bold mb-2 text-gray-800">Wind Speed</h3>
                    <p className="text-4xl font-bold text-orange-700">{data.weather.wind ? data.weather.wind.toFixed(1) + ' m/s' : 'N/A'}</p>
                  </div>
                  <div className="bg-gradient-to-br from-indigo-100 to-purple-200 p-8 rounded-3xl text-center shadow-lg lg:col-span-1">
                    <div className="text-4xl mb-4">{data.weather.condition ? '🌤️' : '🌤️'}</div>
                    <h3 className="text-xl font-bold mb-2 text-gray-800">Condition</h3>
                    <p className="text-xl capitalize">{data.weather.condition || 'Clear'}</p>
                    {data.weather.source === 'historical' && <p className="text-sm text-gray-500 mt-1">Historical Avg</p>}
                  </div>
                  {data.weather.avg_rainfall && (
                    <div className="lg:col-span-4 p-8 bg-gradient-to-r from-green-100 to-emerald-200 rounded-3xl shadow-lg">
                      <h3 className="text-2xl font-bold mb-4 text-gray-800">🌧️ Rainfall Analysis</h3>
                      <ResponsiveContainer width="100%" height={250}>
                        <LineChart data={Array(5).fill({rainfall: data.weather.avg_rainfall})}>
                          <Line type="monotone" dataKey="rainfall" stroke="#059669" strokeWidth={4} dot={false} />
                          <Tooltip formatter={(value) => [`${value.toFixed(1)} mm`, 'Avg Rainfall']} />
                          <YAxis />
                        </LineChart>
                      </ResponsiveContainer>
                      <p className="text-center text-lg mt-4 text-gray-700">Avg: {data.weather.avg_rainfall.toFixed(1)} mm ({data.weather.days} days)</p>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

