# Deployment Guide - African Language AI Tutor
## How to Deploy Your App for Public Use

---

## Overview

This guide covers multiple deployment options for your African Language AI Tutor, from easiest (free) to most advanced (custom server).

---

## Option 1: Streamlit Community Cloud (RECOMMENDED - FREE & EASIEST)

### ✅ Pros:
- **100% FREE** for public apps
- Easiest deployment (3 clicks)
- Automatic updates from GitHub
- Built-in SSL/HTTPS
- No server management needed
- Perfect for demos and MVPs

### ❌ Cons:
- Limited resources (1 GB RAM)
- Public apps only (unless you pay)
- Sleeps after inactivity

### 📋 Step-by-Step Deployment:

#### 1. Prepare Your Repository

Your repository is already set up correctly! But let's verify:

```bash
# Check these files exist:
✓ african_language_tutor.py (main app)
✓ requirements.txt (dependencies)
✓ .gitignore (protects .env)
✓ language_data/ (knowledge bases)
```

#### 2. Create Streamlit Account

1. Go to https://share.streamlit.io/
2. Click "Sign up" or "Continue with GitHub"
3. Authorize Streamlit to access your GitHub

#### 3. Deploy Your App

1. Click "New app" button
2. Fill in the form:
   - **Repository:** `GRACENGARI/MULTILINGUAL-VOICE-AND-TEXT`
   - **Branch:** `main`
   - **Main file path:** `african_language_tutor.py`
   - **App URL:** Choose a custom URL (e.g., `african-language-tutor`)

3. Click "Advanced settings" and add your secrets:
   ```
   GOOGLE_API_KEY = "AIzaSyDE2-nm8Szz9sX4oEWXyZmZibaR-bZR-3w"
   ```

4. Click "Deploy!"

#### 4. Your App is Live! 🎉

Your app will be available at:
```
https://african-language-tutor.streamlit.app
```

**Deployment time:** 2-5 minutes

#### 5. Managing Your Deployed App

- **Update app:** Just push to GitHub - auto-deploys!
- **View logs:** Click "Manage app" → "Logs"
- **Reboot app:** Click "Manage app" → "Reboot"
- **Delete app:** Click "Manage app" → "Delete app"

---

## Option 2: Hugging Face Spaces (FREE & POPULAR)

### ✅ Pros:
- FREE with good resources (16 GB RAM)
- Great for ML/AI apps
- Built-in community features
- Persistent storage
- Good for showcasing

### ❌ Cons:
- Slightly more setup than Streamlit Cloud
- Slower cold starts

### 📋 Step-by-Step Deployment:

#### 1. Create Hugging Face Account
- Go to https://huggingface.co/join
- Sign up (free)

#### 2. Create a New Space
1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Fill in:
   - **Space name:** `african-language-tutor`
   - **License:** Apache 2.0
   - **SDK:** Streamlit
   - **Visibility:** Public

#### 3. Upload Your Files

You can either:

**Option A: Use Git**
```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/african-language-tutor
cd african-language-tutor
cp -r /path/to/your/project/* .
git add .
git commit -m "Initial deployment"
git push
```

**Option B: Use Web Interface**
- Upload files directly through the web UI

#### 4. Add Secrets
1. Go to your Space settings
2. Click "Repository secrets"
3. Add:
   - Name: `GOOGLE_API_KEY`
   - Value: `AIzaSyDE2-nm8Szz9sX4oEWXyZmZibaR-bZR-3w`

#### 5. Your App is Live! 🎉

Your app will be at:
```
https://huggingface.co/spaces/YOUR_USERNAME/african-language-tutor
```

---

## Option 3: Render (FREE TIER AVAILABLE)

### ✅ Pros:
- FREE tier available
- More control than Streamlit Cloud
- Good performance
- Custom domains supported

### ❌ Cons:
- Free tier sleeps after 15 min inactivity
- Slower cold starts (30-60 seconds)

### 📋 Step-by-Step Deployment:

#### 1. Create Render Account
- Go to https://render.com/
- Sign up with GitHub

#### 2. Create New Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Select `MULTILINGUAL-VOICE-AND-TEXT`

#### 3. Configure Service
```
Name: african-language-tutor
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: streamlit run african_language_tutor.py --server.port=$PORT --server.address=0.0.0.0
```

#### 4. Add Environment Variables
```
GOOGLE_API_KEY = AIzaSyDE2-nm8Szz9sX4oEWXyZmZibaR-bZR-3w
```

#### 5. Deploy
- Click "Create Web Service"
- Wait 5-10 minutes for first deployment

Your app will be at:
```
https://african-language-tutor.onrender.com
```

---

## Option 4: Railway (PAID - $5/month)

### ✅ Pros:
- Always on (no sleeping)
- Fast performance
- Easy deployment
- Good for production

### ❌ Cons:
- Costs $5/month minimum
- No free tier anymore

### 📋 Quick Setup:
1. Go to https://railway.app/
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add environment variable: `GOOGLE_API_KEY`
6. Railway auto-detects Streamlit and deploys!

---

## Option 5: Google Cloud Run (PAY-AS-YOU-GO)

### ✅ Pros:
- Scales automatically
- Only pay for usage
- Professional grade
- Custom domains

### ❌ Cons:
- Requires Docker knowledge
- More complex setup
- Costs money (but cheap for low traffic)

### 📋 Setup Overview:

#### 1. Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD streamlit run african_language_tutor.py --server.port=8080 --server.address=0.0.0.0
```

#### 2. Deploy to Cloud Run
```bash
# Install Google Cloud SDK
# Then run:
gcloud run deploy african-language-tutor \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## Option 6: AWS EC2 / DigitalOcean (FULL CONTROL)

### ✅ Pros:
- Complete control
- Can handle high traffic
- Professional deployment
- Custom configurations

### ❌ Cons:
- Most expensive ($5-50/month)
- Requires server management
- Need DevOps knowledge

### 📋 Quick Setup (Ubuntu Server):

```bash
# 1. SSH into your server
ssh user@your-server-ip

# 2. Install dependencies
sudo apt update
sudo apt install python3-pip nginx

# 3. Clone your repository
git clone https://github.com/GRACENGARI/MULTILINGUAL-VOICE-AND-TEXT.git
cd MULTILINGUAL-VOICE-AND-TEXT

# 4. Install Python packages
pip3 install -r requirements.txt

# 5. Create .env file
echo "GOOGLE_API_KEY=AIzaSyDE2-nm8Szz9sX4oEWXyZmZibaR-bZR-3w" > .env

# 6. Run with systemd (keeps app running)
sudo nano /etc/systemd/system/african-tutor.service
```

Add this to the service file:
```ini
[Unit]
Description=African Language Tutor
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/MULTILINGUAL-VOICE-AND-TEXT
ExecStart=/usr/local/bin/streamlit run african_language_tutor.py --server.port=8501
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# 7. Start the service
sudo systemctl start african-tutor
sudo systemctl enable african-tutor

# 8. Configure Nginx as reverse proxy
sudo nano /etc/nginx/sites-available/african-tutor
```

---

## 🎯 RECOMMENDED DEPLOYMENT PATH

### For Your Use Case (Educational App):

**Start with:** Streamlit Community Cloud (FREE)
- Perfect for demos and testing
- Zero cost
- Easy to set up
- Good enough for 100s of users

**Upgrade to:** Hugging Face Spaces (FREE)
- If you need more resources
- Better for ML community
- Still free!

**Go Professional:** Railway or Google Cloud Run
- When you have 1000+ daily users
- Need guaranteed uptime
- Have budget ($5-20/month)

---

## 📊 Comparison Table

| Platform | Cost | Setup Time | Resources | Best For |
|----------|------|------------|-----------|----------|
| **Streamlit Cloud** | FREE | 5 min | 1 GB RAM | Demos, MVPs |
| **Hugging Face** | FREE | 10 min | 16 GB RAM | ML Apps |
| **Render** | FREE/Paid | 15 min | 512 MB RAM | Small Apps |
| **Railway** | $5/mo | 10 min | Good | Production |
| **Cloud Run** | Pay-as-go | 30 min | Scalable | High Traffic |
| **EC2/DO** | $5-50/mo | 1-2 hours | Full Control | Enterprise |

---

## 🚀 QUICK START: Deploy in 5 Minutes

### Using Streamlit Cloud (Easiest):

1. **Go to:** https://share.streamlit.io/
2. **Sign in** with GitHub
3. **Click** "New app"
4. **Enter:**
   - Repository: `GRACENGARI/MULTILINGUAL-VOICE-AND-TEXT`
   - Branch: `main`
   - Main file: `african_language_tutor.py`
5. **Add secret:** 
   - `GOOGLE_API_KEY = "your-key-here"`
6. **Click** "Deploy!"

**Done!** Your app is live at: `https://your-app-name.streamlit.app`

---

## 🔒 Security Best Practices

### 1. Protect Your API Key
- ✅ Use secrets management (not .env in production)
- ✅ Rotate keys regularly
- ✅ Set usage limits in Google Cloud Console

### 2. Add Rate Limiting
```python
# Add to your app
import streamlit as st
from datetime import datetime, timedelta

if 'last_request' not in st.session_state:
    st.session_state.last_request = datetime.now()

# Limit to 1 request per second
if (datetime.now() - st.session_state.last_request).seconds < 1:
    st.warning("Please wait a moment before making another request")
    st.stop()
```

### 3. Monitor Usage
- Set up Google Cloud billing alerts
- Monitor API usage in Google Cloud Console
- Set daily quotas

---

## 📈 Scaling Considerations

### When to Upgrade:

**Stay on Free Tier if:**
- < 100 daily users
- Educational/demo purpose
- Limited budget

**Upgrade to Paid if:**
- > 500 daily users
- Need 24/7 uptime
- Commercial use
- Need custom domain

---

## 🆘 Troubleshooting

### Common Issues:

**1. App won't start**
- Check requirements.txt has all dependencies
- Verify Python version (3.8-3.11)
- Check logs for errors

**2. API key not working**
- Verify secret is set correctly
- Check for extra spaces/quotes
- Regenerate key if needed

**3. App is slow**
- Optimize temperature (already at 0.1 ✓)
- Add caching with `@st.cache_data`
- Reduce max_tokens if needed

**4. Out of memory**
- Upgrade to paid tier
- Optimize vector store loading
- Clear session state regularly

---

## 📞 Support Resources

- **Streamlit Docs:** https://docs.streamlit.io/
- **Streamlit Forum:** https://discuss.streamlit.io/
- **Your GitHub:** https://github.com/GRACENGARI/MULTILINGUAL-VOICE-AND-TEXT

---

## ✅ Pre-Deployment Checklist

Before deploying, ensure:

- [ ] All code is pushed to GitHub
- [ ] requirements.txt is complete
- [ ] .env is in .gitignore
- [ ] API key is valid and has quota
- [ ] App runs locally without errors
- [ ] All features tested
- [ ] README.md is updated
- [ ] License file exists

---

## 🎉 Next Steps After Deployment

1. **Share your app URL** with users
2. **Monitor usage** in first week
3. **Collect feedback** from users
4. **Set up analytics** (optional)
5. **Add custom domain** (optional)
6. **Scale up** if needed

---

**Your app is ready to deploy! Start with Streamlit Cloud - it's free and takes 5 minutes!**

Good luck! 🚀
