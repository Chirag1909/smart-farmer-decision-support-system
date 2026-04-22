const tokenKey = "smart_farmer_token";
const uiThemeKey = "smart_farmer_theme";
const uiDensityKey = "smart_farmer_density";
const uiSidebarKey = "smart_farmer_sidebar";
let profitChart = null;
let revenueCostChart = null;
let yieldPriceChart = null;
let weatherRainfallChart = null;
let weatherTempChart = null;
let profitCropBarChart = null;
let profitRevenueCostLineChart = null;
let profitDistributionPieChart = null;
let mandiPricePerCropChart = null;
let mandiTopMarketsChart = null;
let mandiPriceTrendChart = null;
let recYieldChart = null;
let recPriceChart = null;
let recYieldPriceTrendChart = null;
let currentMandiRows = [];
let mandiSortState = { key: "modal_price", dir: "desc" };

const jsonRequest = async (url, method = "GET", body = null) => {
  const headers = { "Content-Type": "application/json" };
  const token = localStorage.getItem(tokenKey);
  if (token) headers.Authorization = `Bearer ${token}`;
  const response = await fetch(url, { method, headers, body: body ? JSON.stringify(body) : null });
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || "Request failed");
  return data;
};

const setFormMessage = (id, message = "") => {
  const node = document.getElementById(id);
  if (!node) return;
  node.innerText = message;
  node.classList.toggle("show", Boolean(message));
};

const applyUIPreferences = () => {
  const body = document.body;
  const savedTheme = localStorage.getItem(uiThemeKey) || "dark";
  const savedDensity = localStorage.getItem(uiDensityKey) || "comfortable";
  const savedSidebar = localStorage.getItem(uiSidebarKey) || "expanded";

  body.setAttribute("data-theme", savedTheme);
  body.classList.toggle("density-compact", savedDensity === "compact");
  body.classList.toggle("sidebar-collapsed", savedSidebar === "collapsed");

  const themeIcon = document.querySelector("#theme-toggle i");
  if (themeIcon) themeIcon.className = savedTheme === "light" ? "bi bi-sun" : "bi bi-moon-stars";
  const densityIcon = document.querySelector("#density-toggle i");
  if (densityIcon) densityIcon.className = savedDensity === "compact" ? "bi bi-view-list" : "bi bi-distribute-vertical";
  const sidebarIcon = document.querySelector("#sidebar-toggle i");
  if (sidebarIcon) sidebarIcon.className = savedSidebar === "collapsed" ? "bi bi-layout-sidebar-inset-reverse" : "bi bi-layout-sidebar-inset";
};

const bindUIControls = () => {
  const body = document.body;
  const themeBtn = document.getElementById("theme-toggle");
  const densityBtn = document.getElementById("density-toggle");
  const sidebarBtn = document.getElementById("sidebar-toggle");
  const mobileMenuBtn = document.getElementById("mobile-menu-toggle");
  const sidebarBackdrop = document.getElementById("sidebar-backdrop");

  themeBtn?.addEventListener("click", () => {
    const nextTheme = body.getAttribute("data-theme") === "light" ? "dark" : "light";
    localStorage.setItem(uiThemeKey, nextTheme);
    applyUIPreferences();
  });

  densityBtn?.addEventListener("click", () => {
    const nextDensity = body.classList.contains("density-compact") ? "comfortable" : "compact";
    localStorage.setItem(uiDensityKey, nextDensity);
    applyUIPreferences();
  });

  sidebarBtn?.addEventListener("click", () => {
    const nextSidebar = body.classList.contains("sidebar-collapsed") ? "expanded" : "collapsed";
    localStorage.setItem(uiSidebarKey, nextSidebar);
    applyUIPreferences();
  });

  const closeMobileMenu = () => {
    body.classList.remove("mobile-menu-open");
    sidebarBackdrop?.classList.add("hidden");
  };
  mobileMenuBtn?.addEventListener("click", () => {
    const willOpen = !body.classList.contains("mobile-menu-open");
    body.classList.toggle("mobile-menu-open", willOpen);
    sidebarBackdrop?.classList.toggle("hidden", !willOpen);
  });
  sidebarBackdrop?.addEventListener("click", closeMobileMenu);

  window.addEventListener("resize", () => {
    if (window.innerWidth > 1024) closeMobileMenu();
  });
};

const attachAuthForms = () => {
  const loginForm = document.getElementById("login-form");
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const payload = Object.fromEntries(new FormData(loginForm).entries());
      try {
        const result = await jsonRequest("/login", "POST", payload);
        localStorage.setItem(tokenKey, result.token);
        setFormMessage("login-message", "");
        window.location.href = "/dashboard-page";
      } catch (err) {
        setFormMessage("login-message", err.message);
      }
    });
  }

  const registerForm = document.getElementById("register-form");
  if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const payload = Object.fromEntries(new FormData(registerForm).entries());
      try {
        await jsonRequest("/register", "POST", payload);
        setFormMessage("register-message", "");
        window.location.href = "/login-page";
      } catch (err) {
        setFormMessage("register-message", err.message);
      }
    });
  }
};

const setLoading = (show) => {
  document.getElementById("loading")?.classList.toggle("hidden", !show);
};
const inr = (value) => `Rs ${Number(value || 0).toLocaleString("en-IN", { maximumFractionDigits: 2 })}`;
const asNumber = (value) => {
  const parsed = Number(value);
  return Number.isFinite(parsed) ? parsed : 0;
};
const asLabel = (value) => (value === null || value === undefined || value === "" ? "N/A" : value);
const formatDate = (value) => {
  if (!value) return "N/A";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? value : date.toLocaleDateString("en-IN", { day: "2-digit", month: "short" });
};

const fillTable = (tableId, rows, mapRow) => {
  const tbody = document.querySelector(`#${tableId} tbody`);
  tbody.innerHTML = "";
  rows.forEach((row) => {
    const tr = document.createElement("tr");
    tr.innerHTML = mapRow(row);
    tbody.appendChild(tr);
  });
};

const buildChartOptions = () => ({
  responsive: true,
  maintainAspectRatio: false,
  animation: { duration: 850, easing: "easeOutQuart" },
  plugins: { legend: { labels: { color: "#d1d5db" } } },
  scales: {
    x: { ticks: { color: "#a5b4fc" }, grid: { color: "rgba(148,163,184,0.1)" } },
    y: { ticks: { color: "#a5b4fc" }, grid: { color: "rgba(148,163,184,0.1)" } },
  },
});

const renderProfitAnalytics = (rows) => {
  if (!Array.isArray(rows) || !rows.length) return;

  const labels = rows.map((r) => asLabel(r.crop));
  const revenues = rows.map((r) => asNumber(r.expected_revenue));
  const profits = rows.map((r) => asNumber(r.expected_profit));
  const margins = rows.map((r) => asNumber(r.profit_margin));
  const costs = revenues.map((value, idx) => Math.max(0, value - profits[idx]));

  const bestIndex = profits.indexOf(Math.max(...profits));
  const barColors = profits.map((_, idx) => (idx === bestIndex ? "#00ff88" : "#2563eb"));

  document.getElementById("profit-best-crop").innerText = labels[bestIndex];
  document.getElementById("profit-total").innerText = inr(profits.reduce((acc, cur) => acc + cur, 0));
  document.getElementById("profit-avg-margin").innerText = `${(margins.reduce((acc, cur) => acc + cur, 0) / margins.length).toFixed(2)}%`;

  if (profitCropBarChart) profitCropBarChart.destroy();
  profitCropBarChart = new Chart(document.getElementById("profit-crop-bar-chart"), {
    type: "bar",
    data: { labels, datasets: [{ label: "Expected Profit", data: profits, backgroundColor: barColors, borderRadius: 8 }] },
    options: buildChartOptions(),
  });

  if (profitRevenueCostLineChart) profitRevenueCostLineChart.destroy();
  profitRevenueCostLineChart = new Chart(document.getElementById("profit-revenue-cost-line-chart"), {
    type: "line",
    data: {
      labels,
      datasets: [
        { label: "Expected Revenue", data: revenues, borderColor: "#38bdf8", backgroundColor: "rgba(56,189,248,0.2)", tension: 0.3 },
        { label: "Production Cost", data: costs, borderColor: "#f59e0b", backgroundColor: "rgba(245,158,11,0.2)", tension: 0.3 },
      ],
    },
    options: buildChartOptions(),
  });

  if (profitDistributionPieChart) profitDistributionPieChart.destroy();
  profitDistributionPieChart = new Chart(document.getElementById("profit-distribution-pie-chart"), {
    type: "pie",
    data: {
      labels,
      datasets: [
        {
          label: "Profit Distribution",
          data: profits,
          backgroundColor: ["#00ff88", "#2563eb", "#38bdf8", "#f59e0b", "#a855f7", "#ef4444"],
        },
      ],
    },
    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { labels: { color: "#d1d5db" } } } },
  });
};

const renderRecommendationAnalytics = (rows) => {
  if (!Array.isArray(rows) || !rows.length) return;

  const labels = rows.map((r) => asLabel(r.crop));
  const yields = rows.map((r) => asNumber(r.predicted_yield));
  const prices = rows.map((r) => asNumber(r.modal_price));

  const topYieldIndex = yields.indexOf(Math.max(...yields));
  const avgYield = yields.reduce((acc, cur) => acc + cur, 0) / yields.length;
  const avgPrice = prices.reduce((acc, cur) => acc + cur, 0) / prices.length;

  document.getElementById("rec-top-crop").innerText = labels[topYieldIndex];
  document.getElementById("rec-avg-yield").innerText = avgYield.toFixed(2);
  document.getElementById("rec-avg-price").innerText = inr(avgPrice);

  const yieldColors = yields.map((_, idx) => (idx === topYieldIndex ? "#00ff88" : "#2563eb"));
  if (recYieldChart) recYieldChart.destroy();
  recYieldChart = new Chart(document.getElementById("rec-yield-chart"), {
    type: "bar",
    data: {
      labels,
      datasets: [{ label: "Predicted Yield", data: yields, backgroundColor: yieldColors, borderRadius: 8 }],
    },
    options: buildChartOptions(),
  });

  const topPriceIndex = prices.indexOf(Math.max(...prices));
  const priceColors = prices.map((_, idx) => (idx === topPriceIndex ? "#38bdf8" : "#22c55e"));
  if (recPriceChart) recPriceChart.destroy();
  recPriceChart = new Chart(document.getElementById("rec-price-chart"), {
    type: "bar",
    data: {
      labels,
      datasets: [{ label: "Modal Price", data: prices, backgroundColor: priceColors, borderRadius: 8 }],
    },
    options: buildChartOptions(),
  });

  if (recYieldPriceTrendChart) recYieldPriceTrendChart.destroy();
  recYieldPriceTrendChart = new Chart(document.getElementById("rec-yield-price-trend-chart"), {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          label: "Predicted Yield",
          data: yields,
          borderColor: "#00ff88",
          backgroundColor: "rgba(0,255,136,0.2)",
          yAxisID: "y",
          tension: 0.3,
        },
        {
          label: "Modal Price",
          data: prices,
          borderColor: "#2563eb",
          backgroundColor: "rgba(37,99,235,0.2)",
          yAxisID: "y1",
          tension: 0.3,
        },
      ],
    },
    options: {
      ...buildChartOptions(),
      scales: {
        x: { ticks: { color: "#a5b4fc" }, grid: { color: "rgba(148,163,184,0.1)" } },
        y: { type: "linear", position: "left", ticks: { color: "#a5b4fc" }, grid: { color: "rgba(148,163,184,0.1)" } },
        y1: { type: "linear", position: "right", ticks: { color: "#a5b4fc" }, grid: { drawOnChartArea: false } },
      },
    },
  });
};

const applyMandiSorting = () => {
  if (!currentMandiRows.length) return;
  const { key, dir } = mandiSortState;
  const multiplier = dir === "asc" ? 1 : -1;
  const sorted = [...currentMandiRows].sort((a, b) => {
    const av = a[key];
    const bv = b[key];
    if (key === "modal_price") return (asNumber(av) - asNumber(bv)) * multiplier;
    if (key === "date") return (new Date(av).getTime() - new Date(bv).getTime()) * multiplier;
    return String(av || "").localeCompare(String(bv || "")) * multiplier;
  });

  fillTable("mandi-table", sorted, (row) =>
    `<td>${asLabel(row.market)}</td><td>${asLabel(row.district)}</td><td>${asLabel(row.crop)}</td><td>${inr(row.modal_price)}</td><td>${asLabel(row.date)}</td>`
  );
};

const renderMandiAnalytics = (rows) => {
  if (!Array.isArray(rows) || !rows.length) return;

  const highest = rows.reduce((max, row) => (asNumber(row.modal_price) > asNumber(max.modal_price) ? row : max), rows[0]);
  const avgPrice = rows.reduce((acc, row) => acc + asNumber(row.modal_price), 0) / rows.length;

  document.getElementById("mandi-highest-crop").innerText = asLabel(highest.crop);
  document.getElementById("mandi-best-market").innerText = asLabel(highest.market);
  document.getElementById("mandi-average-price").innerText = inr(avgPrice);

  const cropMap = {};
  rows.forEach((row) => {
    const key = asLabel(row.crop);
    cropMap[key] = cropMap[key] || { sum: 0, count: 0 };
    cropMap[key].sum += asNumber(row.modal_price);
    cropMap[key].count += 1;
  });
  const cropLabels = Object.keys(cropMap);
  const cropPrices = cropLabels.map((label) => cropMap[label].sum / cropMap[label].count);

  if (mandiPricePerCropChart) mandiPricePerCropChart.destroy();
  mandiPricePerCropChart = new Chart(document.getElementById("mandi-price-per-crop-chart"), {
    type: "bar",
    data: { labels: cropLabels, datasets: [{ label: "Avg Modal Price", data: cropPrices, backgroundColor: "#2563eb", borderRadius: 8 }] },
    options: buildChartOptions(),
  });

  const topMarkets = [...rows].sort((a, b) => asNumber(b.modal_price) - asNumber(a.modal_price)).slice(0, 10);
  if (mandiTopMarketsChart) mandiTopMarketsChart.destroy();
  mandiTopMarketsChart = new Chart(document.getElementById("mandi-top-markets-chart"), {
    type: "bar",
    data: {
      labels: topMarkets.map((r) => asLabel(r.market)),
      datasets: [{ label: "Modal Price", data: topMarkets.map((r) => asNumber(r.modal_price)), backgroundColor: "#00ff88", borderRadius: 8 }],
    },
    options: buildChartOptions(),
  });

  const dateMap = {};
  rows.forEach((row) => {
    const key = asLabel(row.date);
    if (key === "N/A") return;
    dateMap[key] = dateMap[key] || { sum: 0, count: 0 };
    dateMap[key].sum += asNumber(row.modal_price);
    dateMap[key].count += 1;
  });
  const dateLabels = Object.keys(dateMap).sort((a, b) => new Date(a).getTime() - new Date(b).getTime());
  const datePrices = dateLabels.map((key) => dateMap[key].sum / dateMap[key].count);

  if (mandiPriceTrendChart) mandiPriceTrendChart.destroy();
  mandiPriceTrendChart = new Chart(document.getElementById("mandi-price-trend-chart"), {
    type: "line",
    data: {
      labels: dateLabels.map((date) => formatDate(date)),
      datasets: [{ label: "Avg Price Trend", data: datePrices, borderColor: "#38bdf8", backgroundColor: "rgba(56,189,248,0.2)", tension: 0.25 }],
    },
    options: buildChartOptions(),
  });
};

const loadDashboardData = async () => {
  const state = document.getElementById("state-select").value;
  setLoading(true);
  try {
    const [recommend, profit, history] = await Promise.all([
      jsonRequest("/recommend", "POST", { state, top_k: 5 }),
      jsonRequest("/profit", "POST", { state, top_k: 5 }),
      jsonRequest("/history"),
    ]);

    fillTable("recommend-table", recommend.recommendations, (row) =>
      `<td>${asLabel(row.crop)}</td><td>${asNumber(row.predicted_yield).toFixed(2)}</td><td>${inr(row.modal_price)}</td>`
    );
    renderRecommendationAnalytics(recommend.recommendations);

    fillTable("profit-table", profit.top_crops, (row) =>
      `<td>${asLabel(row.crop)}</td><td>${inr(row.expected_revenue)}</td><td>${inr(Math.max(0, asNumber(row.expected_revenue) - asNumber(row.expected_profit)))}</td><td>${inr(row.expected_profit)}</td><td>${asNumber(row.profit_margin).toFixed(2)}</td>`
    );

    fillTable("history-table", history.history, (row) =>
      `<td>${asLabel(row.state)}</td><td>${asLabel(row.selected_crop)}</td><td>${inr(row.predicted_profit)}</td><td>${asLabel(row.created_at)}</td>`
    );

    const best = profit.best_crop;
    document.getElementById("best-crop").innerText = asLabel(best.crop);
    document.getElementById("best-revenue").innerText = inr(best.expected_revenue);
    document.getElementById("best-profit").innerText = inr(best.expected_profit);
    document.getElementById("best-margin").innerText = `${asNumber(best.profit_margin).toFixed(2)}%`;

    const labels = profit.top_crops.map((r) => asLabel(r.crop));
    const profits = profit.top_crops.map((r) => asNumber(r.expected_profit));
    const revenues = profit.top_crops.map((r) => asNumber(r.expected_revenue));
    const costs = profit.top_crops.map((r) => Math.max(0, asNumber(r.expected_revenue) - asNumber(r.expected_profit)));
    const yields = recommend.recommendations.map((r) => asNumber(r.predicted_yield));
    const prices = recommend.recommendations.map((r) => asNumber(r.modal_price));

    const ctx = document.getElementById("profit-chart");
    if (profitChart) profitChart.destroy();
    profitChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels,
        datasets: [{ label: "Expected Profit", data: profits, backgroundColor: "#14b8a6", borderRadius: 8 }],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { labels: { color: "#d1d5db" } } },
        scales: {
          x: { ticks: { color: "#a5b4fc" }, grid: { color: "rgba(148,163,184,0.1)" } },
          y: { ticks: { color: "#a5b4fc" }, grid: { color: "rgba(148,163,184,0.1)" } },
        },
      },
    });

    const rcCtx = document.getElementById("revenue-cost-chart");
    if (revenueCostChart) revenueCostChart.destroy();
    revenueCostChart = new Chart(rcCtx, {
      type: "bar",
      data: {
        labels,
        datasets: [
          { label: "Revenue", data: revenues, backgroundColor: "#38bdf8", borderRadius: 8 },
          { label: "Estimated Cost", data: costs, backgroundColor: "#f59e0b", borderRadius: 8 },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { labels: { color: "#d1d5db" } } },
        scales: {
          x: { ticks: { color: "#a5b4fc" }, grid: { color: "rgba(148,163,184,0.1)" } },
          y: { ticks: { color: "#a5b4fc" }, grid: { color: "rgba(148,163,184,0.1)" } },
        },
      },
    });

    const ypCtx = document.getElementById("yield-price-chart");
    if (yieldPriceChart) yieldPriceChart.destroy();
    yieldPriceChart = new Chart(ypCtx, {
      type: "line",
      data: {
        labels: recommend.recommendations.map((r) => asLabel(r.crop)),
        datasets: [
          {
            label: "Yield",
            data: yields,
            borderColor: "#22c55e",
            backgroundColor: "rgba(34,197,94,0.2)",
            yAxisID: "y",
            tension: 0.3,
          },
          {
            label: "Price",
            data: prices,
            borderColor: "#f97316",
            backgroundColor: "rgba(249,115,22,0.2)",
            yAxisID: "y1",
            tension: 0.3,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { labels: { color: "#d1d5db" } } },
        scales: {
          x: { ticks: { color: "#a5b4fc" }, grid: { color: "rgba(148,163,184,0.1)" } },
          y: { type: "linear", position: "left", ticks: { color: "#a5b4fc" }, grid: { color: "rgba(148,163,184,0.1)" } },
          y1: { type: "linear", position: "right", ticks: { color: "#a5b4fc" }, grid: { drawOnChartArea: false } },
        },
      },
    });
    renderProfitAnalytics(profit.top_crops);
  } catch (err) {
    alert(err.message);
  } finally {
    setLoading(false);
  }
};

const loadMandi = async () => {
  const state = document.getElementById("state-select").value;
  const crop = document.getElementById("crop-filter").value.trim();
  try {
    const data = await jsonRequest(`/mandi?state=${encodeURIComponent(state)}&crop=${encodeURIComponent(crop)}`);
    currentMandiRows = Array.isArray(data.rows) ? data.rows : [];
    applyMandiSorting();
    renderMandiAnalytics(currentMandiRows);
    document.getElementById("best-mandi").innerText = `Best mandi: ${asLabel(data.best.market)} (${inr(data.best.modal_price)})`;
  } catch (err) {
    alert(err.message);
  }
};

const loadWeather = async () => {
  const state = document.getElementById("state-select").value;
  try {
    const data = await jsonRequest(`/weather?state=${encodeURIComponent(state)}`);
    const weather = data.weather;
    if (weather.error) {
      document.getElementById("weather-error").innerText = weather.error;
      return;
    }
    document.getElementById("weather-temp").innerText = `${asNumber(weather.temperature).toFixed(1)} C`;
    document.getElementById("weather-humidity").innerText = `${asNumber(weather.humidity).toFixed(0)}%`;
    document.getElementById("weather-condition").innerText = asLabel(weather.condition);
    document.getElementById("weather-source").innerText = asLabel(weather.source);
    document.getElementById("weather-rain-total").innerText = `${asNumber(weather.rainfall_summary?.next_7_days_total_mm).toFixed(1)} mm`;
    document.getElementById("weather-rain-avg").innerText = `${asNumber(weather.rainfall_summary?.next_7_days_avg_mm).toFixed(1)} mm/day`;
    document.getElementById("weather-rain-max").innerText = `${asNumber(weather.rainfall_summary?.max_daily_mm).toFixed(1)} mm`;

    const forecast = Array.isArray(weather.forecast) ? weather.forecast : [];
    const labels = forecast.map((row) => formatDate(row.date));
    const rainValues = forecast.map((row) => asNumber(row.rainfall_mm));
    const maxTempValues = forecast.map((row) => asNumber(row.temp_max));
    const minTempValues = forecast.map((row) => asNumber(row.temp_min));

    const rainCtx = document.getElementById("weather-rainfall-chart");
    if (weatherRainfallChart) weatherRainfallChart.destroy();
    weatherRainfallChart = new Chart(rainCtx, {
      type: "bar",
      data: {
        labels,
        datasets: [
          {
            label: "Rainfall (mm)",
            data: rainValues,
            backgroundColor: "#38bdf8",
            borderRadius: 8,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { labels: { color: "#d1d5db" } } },
        scales: {
          x: { ticks: { color: "#a5b4fc" }, grid: { color: "rgba(148,163,184,0.1)" } },
          y: { ticks: { color: "#a5b4fc" }, grid: { color: "rgba(148,163,184,0.1)" } },
        },
      },
    });

    const tempCtx = document.getElementById("weather-temp-chart");
    if (weatherTempChart) weatherTempChart.destroy();
    weatherTempChart = new Chart(tempCtx, {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            label: "Max Temp (C)",
            data: maxTempValues,
            borderColor: "#f97316",
            backgroundColor: "rgba(249,115,22,0.2)",
            tension: 0.35,
          },
          {
            label: "Min Temp (C)",
            data: minTempValues,
            borderColor: "#22d3ee",
            backgroundColor: "rgba(34,211,238,0.2)",
            tension: 0.35,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { labels: { color: "#d1d5db" } } },
        scales: {
          x: { ticks: { color: "#a5b4fc" }, grid: { color: "rgba(148,163,184,0.1)" } },
          y: { ticks: { color: "#a5b4fc" }, grid: { color: "rgba(148,163,184,0.1)" } },
        },
      },
    });

    document.getElementById("weather-error").innerText = "";
  } catch (err) {
    document.getElementById("weather-error").innerText = err.message;
  }
};

const attachDashboard = async () => {
  const stateSelect = document.getElementById("state-select");
  if (!stateSelect) return;
  const token = localStorage.getItem(tokenKey);
  if (!token) window.location.href = "/login-page";
  applyUIPreferences();
  bindUIControls();

  try {
    const data = await jsonRequest("/dashboard");
    data.states.forEach((state) => {
      const option = document.createElement("option");
      option.value = state;
      option.innerText = state;
      stateSelect.appendChild(option);
    });
    await loadDashboardData();
    await loadWeather();
  } catch {
    localStorage.removeItem(tokenKey);
    window.location.href = "/login-page";
  }

  document.getElementById("refresh-btn").addEventListener("click", loadDashboardData);
  document.getElementById("state-select").addEventListener("change", async () => {
    await loadDashboardData();
    await loadWeather();
  });
  document.getElementById("load-mandi-btn").addEventListener("click", loadMandi);
  document.querySelectorAll("#mandi-table thead th[data-sort]").forEach((header) => {
    header.addEventListener("click", () => {
      const key = header.dataset.sort;
      if (mandiSortState.key === key) {
        mandiSortState.dir = mandiSortState.dir === "asc" ? "desc" : "asc";
      } else {
        mandiSortState = { key, dir: key === "modal_price" ? "desc" : "asc" };
      }
      applyMandiSorting();
    });
  });
  document.getElementById("logout-btn").addEventListener("click", () => {
    localStorage.removeItem(tokenKey);
    window.location.href = "/login-page";
  });

  document.querySelectorAll(".nav-item").forEach((btn) => {
    btn.addEventListener("click", async () => {
      document.querySelectorAll(".nav-item").forEach((b) => b.classList.remove("active"));
      btn.classList.add("active");
      document.getElementById("view-title").innerText = btn.innerText;
      document.querySelectorAll(".view-section").forEach((section) => section.classList.add("hidden"));
      const activeSection = document.getElementById(btn.dataset.view);
      activeSection.classList.remove("hidden");
      if (btn.dataset.view === "weather") await loadWeather();
      if (btn.dataset.view === "mandi") await loadMandi();
      if (btn.dataset.view === "history") await loadDashboardData();
      if (window.innerWidth <= 1024) {
        document.body.classList.remove("mobile-menu-open");
        document.getElementById("sidebar-backdrop")?.classList.add("hidden");
      }
    });
  });
};

attachAuthForms();
attachDashboard();
