# 🚀 Quick Start Guide - African Language AI Tutor

## ⚡ 5-Minute Setup

### 1. **Get Google AI API Key** (2 minutes)
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key"
3. Copy the generated key

### 2. **Configure Environment** (1 minute)
```bash
# Edit the .env file and add your API key
GOOGLE_API_KEY='paste_your_actual_api_key_here'
```

### 3. **Install & Run** (2 minutes)
```bash
# Option A: Automated setup
python setup.py

# Option B: Manual setup
pip install -r requirements.txt
streamlit run african_language_tutor.py
```

## 🎯 First Steps

### Choose Your Language
- **Kiswahili** - "Hujambo! Karibu kwenye mfumo wa kujifunza Kiswahili"
- **Kikuyu** - "Wĩ mwega! Ũkĩrĩte gũkũ kũruta Kikuyu"
- **Luo** - "Oyawore! Rwaki e puonj Luo"
- **Kalenjin** - "Chamge! Boisho ak kole Kalenjin"

### Try These Examples

#### 💬 Chat Mode
```
"What does 'nyumba' mean in Kiswahili?"
"How do I say 'I am learning' in Kikuyu?"
"Check this sentence: Mimi ninasoma kitabu"
"Teach me Luo greetings"
```

#### 🎯 Quiz Mode
- Click "Generate New Quiz"
- Answer vocabulary and grammar questions
- Get instant feedback

#### 📖 Vocabulary Mode
- Search for words in English or target language
- Browse by categories (Family, Food, Colors, etc.)
- See usage examples and cultural context

## 🛠️ Troubleshooting

### Common Issues

**❌ "GOOGLE_API_KEY is not set"**
```bash
# Solution: Add your API key to .env file
GOOGLE_API_KEY='your_actual_key_here'
```

**❌ "Module not found" errors**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**❌ "Language data not found"**
```bash
# Solution: Ensure language_data/ folder exists with JSON files
python demo_script.py  # Test data loading
```

### Verify Setup
```bash
# Test without UI
python demo_script.py

# Check dependencies
python -c "import streamlit, langchain; print('✅ Ready!')"
```

## 🎓 Learning Tips

### Effective Usage
1. **Start Simple**: Begin with basic vocabulary
2. **Ask Questions**: Use natural language queries
3. **Practice Regularly**: Try different modes daily
4. **Cultural Context**: Ask about when/how to use phrases
5. **Corrections**: Submit sentences for grammar checking

### Sample Learning Session
```
1. "Hello, I want to learn Kiswahili greetings"
2. "What's the difference between 'hujambo' and 'habari'?"
3. "How do I respond to 'habari yako'?"
4. "Give me a quiz on Kiswahili greetings"
5. "Check this: 'Habari yako, mimi ni mzuri'"
```

## 📱 Interface Overview

### Main Navigation
- **Language Selection**: Choose your target language
- **Mode Switcher**: Chat, Quiz, or Vocabulary
- **Sidebar**: Quick tips and settings

### Chat Interface
- **Input Box**: Type your questions naturally
- **History**: See previous conversations
- **Clear Button**: Start fresh conversation

### Features
- **🔍 Smart Search**: Find words and concepts
- **🎯 Dynamic Quizzes**: AI-generated practice
- **📚 Rich Examples**: Real usage scenarios
- **🌍 Cultural Context**: Appropriate usage guidance

## 🎯 Next Steps

### Explore Features
- [ ] Try all four languages
- [ ] Test different learning modes
- [ ] Ask about grammar rules
- [ ] Practice with quizzes
- [ ] Explore vocabulary categories

### Advanced Usage
- [ ] Mix languages in questions (code-switching)
- [ ] Ask for alternative sentence constructions
- [ ] Request cultural explanations
- [ ] Practice conversational scenarios

### Contribute
- [ ] Report incorrect information
- [ ] Suggest new vocabulary
- [ ] Share learning experiences
- [ ] Help improve translations

## 📞 Support

### Getting Help
- **Demo Issues**: Run `python demo_script.py`
- **Setup Problems**: Run `python setup.py`
- **API Issues**: Check your Google AI API key
- **Feature Requests**: See PROJECT_OVERVIEW.md

### Resources
- **README.md**: Complete documentation
- **PROJECT_OVERVIEW.md**: Technical details
- **Language JSON files**: Raw knowledge data

---

**Ready to start learning? Choose your language and begin your African language journey! 🌍✨**