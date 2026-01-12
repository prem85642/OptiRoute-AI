# Deployment Guide: Render.com

## Quick Deploy (5 Minutes)

### Step 1: Render Account
1. Go to: https://render.com
2. Click "Sign Up" → "Sign up with GitHub" (easiest!)
3. Authorize Render

### Step 2: Create Web Service
1. Dashboard → Click "New +" → "Web Service"
2. Connect your repository: `prem85642/OptiRoute-AI`
3. Click "Connect"

### Step 3: Configuration

Fill in these exact values:

**Name**: `optiroute-ai`

**Region**: Singapore (or closest to you)

**Branch**: `master`

**Build Command**:
```
pip install -r requirements.txt
```

**Start Command**:
```
uvicorn src.api.main:app --host 0.0.0.0 --port $PORT
```

**Instance Type**: Free

### Step 4: Environment Variables

Click "Add Environment Variable":

**Key**: `HF_API_TOKEN`  
**Value**: `hf_your_actual_token_here`

(Get from: https://huggingface.co/settings/tokens)

### Step 5: Deploy!

1. Click "Create Web Service"
2. Wait 3-5 minutes (watch build logs)
3. Status changes to "Live" = Success! ✅

### Step 6: Test Your Live App

Your URL will be: `https://optiroute-ai.onrender.com`

Open in browser → Should see OptiRoute AI interface!

---

## Troubleshooting

### Build Failed?
**Check**: Build command is exactly:
```
pip install -r requirements.txt
```

### App Not Starting?
**Check**: Start command is exactly:
```
uvicorn src.api.main:app --host 0.0.0.0 --port $PORT
```

### HuggingFace API Error?
**Check**: Environment variable `HF_API_TOKEN` is set correctly

### Slow First Request?
**Normal**: Free tier has cold starts (10-15 seconds first time)

---

## Free Tier Limits

- 750 hours/month (enough for demo!)
- Sleeps after 15 minutes of inactivity
- First request after sleep: 10-15 seconds
- Subsequent requests: Fast!

## Upgrading (Optional)

For instant wake-up: $7/month

---

## Post-Deployment

### Your Live URLs:
- Main App: `https://optiroute-ai.onrender.com`
- Metrics: `https://optiroute-ai.onrender.com/metrics`
- Health: `https://optiroute-ai.onrender.com/health`

### Share With:
- Recruiters
- Portfolio
- LinkedIn
- Resume

**Live demo > screenshots!** 🚀
