# Grafana Dashboard Setup Guide

## Quick Start

### Step 1: Start Prometheus (Already Running ✓)
Prometheus is collecting metrics from OptiRoute AI at `http://localhost:9090`

### Step 2: Start Grafana
```powershell
cd "d:\project1\freelancer\OptiRoute AI - Copy\grafana\bin"
.\grafana-server.exe
```

Wait for the message: `HTTP Server Listen` (usually 30 seconds)

### Step 3: Access Grafana
1. Open browser: http://localhost:3000
2. Login with:
   - Username: `admin`
   - Password: `admin`
   - (You'll be asked to change it - you can skip)

### Step 4: Add Prometheus Data Source
1. Click **Settings** (gear icon) → **Data Sources**
2. Click **Add data source**
3. Select **Prometheus**
4. Set URL: `http://localhost:9090`
5. Click **Save & Test** (should show green checkmark)

### Step 5: Import Dashboard
1. Click **Dashboards** (four squares icon) → **Import**
2. Click **Upload JSON file**
3. Select: `d:\project1\freelancer\OptiRoute AI - Copy\grafana\dashboards\optiRoute_dashboard.json`
4. Click **Load**
5. Select Prometheus data source
6. Click **Import**

---

## Dashboard Panels Explained

### 📊 Total Cost (USD)
- **What**: Cumulative spend across all providers
- **Color Coding**:
  - Green: < $0.01
  - Yellow: $0.01 - $0.10
  - Red: > $0.10

### 📈 Cost by Provider (Time Series)
- **What**: Real-time cost rate per provider
- **Legend**: Shows local_mock_gpu vs huggingface_api

### ⚡ Cache Hit Rate (Gauge)
- **What**: Percentage of requests served from cache
- **Good**: > 80% (green)
- **Average**: 50-80% (yellow)
- **Poor**: < 50% (red)

### 🕐 Request Latency P95
- **What**: 95th percentile response time
- **Target**: < 2 seconds

### 🚀 Requests Per Second
- **What**: Traffic breakdown by endpoint
- **Shows**: `/generate` load in real-time

### 🥧 Cache Events (Pie Chart)
- **What**: Visual split of cache hits vs misses

### ❌ Error Rate
- **What**: 5xx errors per second
- **Target**: 0 (green)

### 💰 Cost Saved by Caching
- **What**: Estimated savings from cache hits
- **Formula**: `cache_hits × average_cost_per_request`

---

## Generating Test Traffic

Run Locust to populate the dashboard:

```powershell
cd "d:\project1\freelancer\OptiRoute AI - Copy"
.venv\Scripts\python -m locust -f src/simulation/locustfile.py --headless -u 100 -r 10 --run-time 5m --host http://localhost:8000
```

You'll see the dashboard panels update in real-time!

---

## Troubleshooting

### Dashboard shows "No Data"
- Check OptiRoute AI is running: http://localhost:8000/health
- Verify Prometheus is scraping: http://localhost:9090/targets
- Confirm Prometheus data source is green

### Grafana won't start
- Check if port 3000 is free: `netstat -ano | findstr :3000`
- Look for error in terminal output

### Metrics not updating
- Refresh interval is 5 seconds
- Run some requests to OptiRoute AI to generate data

---

## Next Steps

1. **Create Alerts**: Set budget thresholds
2. **Export Dashboard**: Share JSON with team
3. **Add Variables**: Filter by provider, time range
4. **Custom Panels**: Add circuit breaker status

**Pro Tip**: Set refresh to "5s" (top-right) for live demo effect!
