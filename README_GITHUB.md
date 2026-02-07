# 🌍 African Language AI Tutor

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Google Gemini](https://img.shields.io/badge/Powered%20by-Google%20Gemini-orange)](https://ai.google.dev/)

An AI-powered language learning platform focused on African languages, helping learners master grammar, vocabulary, and sentence construction using RAG (Retrieval-Augmented Generation) and Google Gemini AI.

![African Language Tutor](https://img.shields.io/badge/Languages-Kiswahili%20%7C%20Kikuyu%20%7C%20Luo%20%7C%20Kalenjin-brightgreen)

## 🎯 Problem Statement

Many learners in African contexts want to strengthen their grammar, vocabulary, and sentence construction in their local languages, but there are very few digital tools available compared to English or other global languages. Traditional language learning apps often neglect indigenous languages, leaving a gap for students, young people, and adults who want to improve literacy and communication skills in their mother tongue.

## ✨ Features

### 🤖 AI-Powered Tutoring
- **Grammar Explanations**: Understand sentence structure, verb conjugations, and language rules
- **Vocabulary Building**: Learn new words with meanings, pronunciation, and usage examples
- **Sentence Correction**: Get feedback on your writing with explanations and alternatives
- **Cultural Context**: Learn about the cultural significance and proper usage

### 🗣️ Supported Languages
- **Kiswahili** - East African lingua franca
- **Kikuyu** - Central Kenya, Bantu family
- **Luo** - Western Kenya/Tanzania, Nilotic family
- **Kalenjin** - Rift Valley Kenya, Nilotic family

### 🎮 Interactive Learning
- **💬 Chat Tutor**: Conversational AI assistance
- **🎯 Quiz Practice**: AI-generated practice questions
- **📖 Vocabulary Builder**: Word exploration by category
- **🎤 Voice Support**: Text-to-speech for pronunciation

### 🌐 Key Capabilities
- **Code-switching Support**: Natural mixing of English and local languages
- **Multilingual Scaffolding**: Ask in English, get answers in target language (and vice versa)
- **RAG Architecture**: Reduces AI hallucination with curated knowledge bases
- **Cultural Sensitivity**: Includes proper usage and cultural context

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google AI API key ([Get one here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/african-language-tutor.git
   cd african-language-tutor
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your Google API key
   ```

5. **Run the application**
   ```bash
   streamlit run african_language_tutor.py
   ```

6. **Open your browser**
   - Navigate to `http://localhost:8501`

## 📚 Usage Examples

### Vocabulary Learning
```
User: "What does 'nyumba' mean in Kiswahili?"
Tutor: "'Nyumba' means 'house' in Kiswahili. It belongs to the N-N noun class.
       Plural: nyumba (same form)
       Example: Nyumba yangu ni kubwa (My house is big)"
```

### Grammar Correction
```
User: "Check this sentence: 'Mimi book ninasoma'"
Tutor: "There's a word order issue. In Kiswahili, use SVO structure:
       Correct: 'Mimi ninasoma kitabu' (I am reading a book)
       'Book' should be 'kitabu' in Kiswahili."
```

### Cultural Context
```
User: "When do I use 'hujambo' vs 'habari'?"
Tutor: "'Hujambo' is more formal and respectful, used with elders.
       'Habari' is casual and friendly, used with peers.
       This shows the importance of respect in Kiswahili culture."
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **AI/ML**: Google Gemini 2.5 Flash
- **Vector Database**: FAISS
- **Embeddings**: Google Generative AI Embeddings
- **Framework**: LangChain
- **Voice**: gTTS (Google Text-to-Speech)
- **Data**: JSON-based knowledge bases

## 📁 Project Structure

```
african-language-tutor/
├── african_language_tutor.py    # Main application
├── requirements.txt             # Python dependencies
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
├── language_data/              # Knowledge bases
│   ├── kiswahili_knowledge.json
│   ├── kikuyu_knowledge.json
│   ├── luo_knowledge.json
│   └── kalenjin_knowledge.json
├── setup.py                    # Setup automation
├── demo_script.py             # Demo without UI
├── test_api_key.py            # API key tester
├── README.md                  # Documentation
├── QUICK_START.md            # Quick start guide
├── PROJECT_OVERVIEW.md       # Technical overview
└── VOICE_FEATURES_GUIDE.md   # Voice features guide
```

## 🎓 Why RAG Over Fine-tuning?

This project uses **Retrieval-Augmented Generation (RAG)** instead of fine-tuning because:

✅ **Cost-Effective**: No expensive training required  
✅ **Real-time Updates**: Add new knowledge instantly  
✅ **Accurate**: Grounded in curated knowledge bases  
✅ **Controllable**: You control exactly what the AI knows  
✅ **Scalable**: Easy to add new languages  
✅ **Reliable**: Reduces hallucination significantly  

Perfect for underserved languages with limited training data!

## 🌟 Key Innovations

### 1. **African Language Focus**
First AI tutor specifically designed for African languages with cultural context

### 2. **RAG Architecture**
Uses curated knowledge bases to ensure accuracy and reduce hallucination

### 3. **Code-switching Support**
Naturally handles mixed language input (English + local language)

### 4. **Cultural Sensitivity**
Includes proper usage, respect patterns, and cultural context

### 5. **Voice Integration**
Text-to-speech for pronunciation practice

### 6. **Community-Driven**
Designed for easy contribution by linguists and native speakers

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Areas for Contribution
- **Language Experts**: Expand vocabulary and grammar rules
- **Audio Content**: Record pronunciation guides
- **UI/UX**: Improve the learning interface
- **Testing**: Validate with native speakers
- **Documentation**: Enhance learning materials

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Adding New Languages
1. Create a knowledge base JSON file in `language_data/`
2. Add language configuration to `SUPPORTED_LANGUAGES`
3. Include grammar rules, vocabulary, and cultural context

## 📊 Roadmap

### Phase 1: Core Enhancement ✅
- [x] RAG-based architecture
- [x] 4 African languages
- [x] Voice features (TTS)
- [x] Interactive quiz mode

### Phase 2: Advanced Features 🚧
- [ ] Speech recognition (voice input)
- [ ] Pronunciation assessment
- [ ] Progress tracking
- [ ] Offline mode

### Phase 3: Expansion 📅
- [ ] More African languages
- [ ] Mobile applications
- [ ] Gamification
- [ ] Teacher dashboard

## 🎯 Impact Goals

- **Bridge digital divide** in African language education
- **Preserve linguistic heritage** through digital tools
- **Empower learners** with AI-assisted instruction
- **Support multilingual education** in African contexts

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Google AI for providing the Gemini API
- African language communities for their rich linguistic heritage
- Open source contributors and language preservation advocates

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/african-language-tutor/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/african-language-tutor/discussions)
- **Documentation**: See `README.md`, `QUICK_START.md`, and `PROJECT_OVERVIEW.md`

## 🌍 Mission

To bridge the digital divide in African language education and promote the use of indigenous languages in digital spaces while preserving linguistic heritage for future generations.

---

**Made with ❤️ for African language learners**

[![Star this repo](https://img.shields.io/github/stars/yourusername/african-language-tutor?style=social)](https://github.com/yourusername/african-language-tutor)
[![Fork this repo](https://img.shields.io/github/forks/yourusername/african-language-tutor?style=social)](https://github.com/yourusername/african-language-tutor/fork)