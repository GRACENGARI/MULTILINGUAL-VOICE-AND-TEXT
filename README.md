# 🌍 African Language AI Tutor

An AI-powered language learning platform focused on African languages, helping learners master grammar, vocabulary, and sentence construction in their local languages.

## 🎯 Overview

This project addresses the gap in digital language learning tools for African languages. While many apps focus on global languages like English, French, or Spanish, there are very few resources for indigenous African languages. Our AI tutor provides personalized instruction for:

- **Kiswahili** - Widely spoken across East Africa
- **Kikuyu** - Spoken by the Kikuyu people of central Kenya  
- **Luo** - Spoken by the Luo people of Kenya and Tanzania
- **Kalenjin** - Spoken by the Kalenjin people of Kenya

## ✨ Features

### 🤖 AI-Powered Tutoring
- **Grammar Explanations**: Understand sentence structure, verb conjugations, and language rules
- **Vocabulary Building**: Learn new words with meanings, pronunciation, and usage examples
- **Sentence Correction**: Get feedback on your writing with explanations and alternatives
- **Cultural Context**: Learn about the cultural significance and proper usage of words and phrases

### 🗣️ Multilingual Support
- **Code-switching Friendly**: Natural mixing of English and local languages
- **Bidirectional Learning**: Ask questions in English, get answers in the target language (and vice versa)
- **Scaffolded Learning**: Gradual transition from familiar to target language

### 🎮 Interactive Learning
- **Dynamic Quizzes**: AI-generated practice questions
- **Conversation Practice**: Role-play scenarios and dialogues
- **Progress Tracking**: Monitor your learning journey
- **Mistake Learning**: System learns from corrections to improve over time

### 🌐 Accessibility Features
- **Offline Capability**: Core features work without internet (planned)
- **Low Bandwidth Mode**: Optimized for rural contexts
- **Speech Recognition**: Voice input for pronunciation practice (planned)
- **Text-to-Speech**: Audio pronunciation guides (planned)

## 🛠️ Technology Stack

- **Frontend**: Streamlit for interactive web interface
- **AI/ML**: Google Gemini AI for language understanding and generation
- **Vector Database**: FAISS for efficient knowledge retrieval
- **Embeddings**: Google Generative AI Embeddings
- **Framework**: LangChain for AI application orchestration
- **Speech**: SpeechRecognition, gTTS, pyttsx3 for audio features
- **Data**: JSON-based knowledge bases for each language

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Google AI API key (for Gemini)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
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
   Create a `.env` file in the project root:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run african_language_tutor.py
   ```

### Getting a Google AI API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key to your `.env` file

## 📚 How to Use

### 1. Select Your Language
Choose from Kiswahili, Kikuyu, Luo, or Kalenjin on the main page.

### 2. Choose Learning Mode
- **💬 Chat Tutor**: Ask questions and get personalized explanations
- **🎯 Quiz Practice**: Test your knowledge with generated quizzes  
- **📖 Vocabulary Builder**: Explore words by category or search

### 3. Start Learning
- Ask about word meanings: "What does 'nyumba' mean?"
- Get grammar help: "How do I conjugate 'kusoma' in past tense?"
- Check sentences: "Is this correct: 'Mimi ninasoma kitabu'?"
- Request practice: "Give me a quiz on Kiswahili greetings"

## 🗂️ Project Structure

```
african-language-tutor/
├── african_language_tutor.py    # Main application
├── requirements.txt             # Python dependencies
├── .env                        # Environment variables (create this)
├── language_data/              # Knowledge bases
│   ├── kiswahili_knowledge.json
│   ├── kikuyu_knowledge.json
│   ├── luo_knowledge.json
│   └── kalenjin_knowledge.json
├── README.md                   # This file
└── .devcontainer/             # Development container config
    └── devcontainer.json
```

## 🎓 Learning Examples

### Vocabulary Learning
```
User: "What does 'mtu' mean in Kiswahili?"
Tutor: "'Mtu' means 'person' in Kiswahili. It belongs to the M-WA noun class.
       Plural: watu (people)
       Example: Mtu huyu ni mwalimu (This person is a teacher)"
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
Tutor: "'Hujambo' is more formal and respectful, used with elders or in formal settings.
       'Habari' is casual and friendly, used with peers.
       Both show the importance of respect in Kiswahili culture."
```

## 🔧 Development

### Adding New Languages
1. Create a knowledge base JSON file in `language_data/`
2. Add language configuration to `SUPPORTED_LANGUAGES` in the main app
3. Include grammar rules, vocabulary, and cultural context

### Extending Features
- **Speech Recognition**: Integrate with `speech_recognition` library
- **Advanced Quizzes**: Add more question types and difficulty levels
- **Progress Tracking**: Implement user profiles and learning analytics
- **Offline Mode**: Cache models and knowledge bases locally

## 🤝 Contributing

We welcome contributions! Areas where help is needed:

- **Language Experts**: Help expand vocabulary and grammar rules
- **Audio Content**: Record pronunciation guides
- **UI/UX**: Improve the learning interface
- **Testing**: Test with native speakers
- **Documentation**: Improve learning materials

## 🌟 Key Challenges Addressed

1. **Limited Resources**: Provides digital tools for underserved languages
2. **Code-switching**: Naturally handles mixed language input
3. **Cultural Sensitivity**: Includes cultural context and appropriate usage
4. **Accessibility**: Designed for low-bandwidth and offline use
5. **Quality Control**: Reduces AI hallucination through knowledge bases
6. **Community Learning**: Allows users to flag and correct mistakes

## 🎯 Future Roadmap

- [ ] **Speech Integration**: Voice input and pronunciation feedback
- [ ] **Mobile App**: Native mobile applications
- [ ] **Community Features**: User-generated content and corrections
- [ ] **Advanced Analytics**: Detailed learning progress tracking
- [ ] **More Languages**: Expand to other African languages
- [ ] **Gamification**: Badges, streaks, and learning challenges
- [ ] **Teacher Dashboard**: Tools for educators and language instructors

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google AI for providing the Gemini API
- The African language communities for their rich linguistic heritage
- Open source contributors and language preservation advocates

## 📞 Support

For questions, suggestions, or issues:
- Create an issue on GitHub
- Contact the development team
- Join our community discussions

---

**Mission**: To bridge the digital divide in African language education and promote the use of indigenous languages in digital spaces while preserving linguistic heritage for future generations.