# OpenAI API Setup Guide

Your app has been migrated from Google Gemini to OpenAI!

## ✅ What Changed:

- **Old:** Google Gemini API (gemini-2.5-flash)
- **New:** OpenAI API (gpt-3.5-turbo)

## 🔑 Setup Your OpenAI API Key:

### Step 1: Get Your OpenAI API Key
1. Go to: https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (it starts with `sk-...`)

### Step 2: Update Your .env File
Open `.env` and replace with your OpenAI key:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

### Step 3: Update Streamlit Cloud (if deployed)
1. Go to your Streamlit Cloud app settings
2. Go to "Secrets" section
3. Replace with:
```toml
OPENAI_API_KEY = "sk-your-actual-key-here"
```

### Step 4: Restart the App
```bash
streamlit run african_language_tutor.py
```

## 💰 Pricing:

OpenAI GPT-3.5-Turbo is very affordable:
- **Input:** $0.50 per 1M tokens
- **Output:** $1.50 per 1M tokens

For your app usage, this will cost pennies per day!

## 🎉 Benefits:

✅ No more "API key leaked" errors  
✅ More reliable API  
✅ Better global availability  
✅ Faster response times  
✅ Better language support  

## 🔒 Security:

- Never share your API key
- Keep it in `.env` file (already in `.gitignore`)
- Use Streamlit secrets for cloud deployment
- Monitor usage at: https://platform.openai.com/usage

---

**Your app is now ready to use with OpenAI!** 🚀
