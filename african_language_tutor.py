import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from dotenv import load_dotenv
import os
import json
import tempfile
import random
import time
from gtts import gTTS
import base64
from io import BytesIO

# Load environment variables
load_dotenv(override=True)  # Force reload

# Try to get API key from multiple sources (for different deployment platforms)
google_api_key = None

# 1. Try Streamlit secrets (for Streamlit Cloud deployment)
try:
    google_api_key = st.secrets["GOOGLE_API_KEY"]
except:
    pass

# 2. Try environment variable (for local development and other platforms)
if not google_api_key:
    google_api_key = os.getenv("GOOGLE_API_KEY")

# Check if API key is loaded (without displaying it)
if not google_api_key:
    st.sidebar.error("❌ API Key not found! Please check your .env file or Streamlit secrets.")


if not google_api_key:
    st.error("⚠️ GOOGLE_API_KEY is not set. Please check your .env file.")
    st.info("""
    **To fix this:**
    1. Make sure .env file exists in the project root
    2. Add this line: GOOGLE_API_KEY=your_actual_key_here
    3. Restart the application
    """)
    st.stop()

# Set page config
st.set_page_config(
    page_title="African Language Tutor",
    page_icon="🌍",
    layout="wide"
)

# Custom CSS - Enhanced Modern UI
st.markdown("""
<style>
/* Main styling */
.main-header {
    text-align: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-size: 3.5rem;
    margin-bottom: 0.5rem;
    font-weight: 900;
    letter-spacing: -1px;
}
.sub-header {
    text-align: center;
    color: #6c757d;
    font-size: 1.3rem;
    margin-bottom: 3rem;
    font-weight: 300;
}

/* Chat messages */
.chat-message {
    padding: 1.5rem;
    border-radius: 1.2rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    animation: slideIn 0.3s ease-out;
}
.chat-message.user {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    margin-left: 2rem;
}
.chat-message.assistant {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    margin-right: 2rem;
}

/* Language selection cards */
.language-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 1rem;
    margin: 1rem 0;
    color: white;
    text-align: center;
    box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    cursor: pointer;
}
.language-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 24px rgba(102, 126, 234, 0.6);
}
.language-card h3 {
    font-size: 1.8rem;
    margin-bottom: 0.5rem;
}
.language-card p {
    font-size: 1rem;
    opacity: 0.9;
}

/* Feature boxes */
.feature-box {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    padding: 2rem;
    border-radius: 1rem;
    border-left: 5px solid #667eea;
    margin: 1rem 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: transform 0.2s ease;
}
.feature-box:hover {
    transform: translateX(5px);
}
.feature-box h4 {
    color: #667eea;
    font-size: 1.3rem;
    margin-bottom: 0.5rem;
}

/* Quiz styling */
.quiz-question {
    background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
    padding: 1.5rem;
    border-radius: 1rem;
    border-left: 5px solid #2196f3;
    margin: 1rem 0;
    box-shadow: 0 4px 6px rgba(33, 150, 243, 0.2);
}
.quiz-question h4 {
    color: #1976d2;
    margin-bottom: 1rem;
}

/* Correction box */
.correction-box {
    background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
    padding: 1.5rem;
    border-radius: 1rem;
    border-left: 5px solid #ff9800;
    margin: 1rem 0;
    box-shadow: 0 4px 6px rgba(255, 152, 0, 0.2);
}

/* Animations */
@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Buttons enhancement */
.stButton>button {
    border-radius: 0.8rem;
    padding: 0.6rem 2rem;
    font-weight: 600;
    transition: all 0.3s ease;
    border: none;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
}

/* Sidebar styling */
.css-1d391kg {
    background: linear-gradient(180deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* Input fields */
.stTextInput>div>div>input {
    border-radius: 0.8rem;
    border: 2px solid #e0e0e0;
    padding: 0.8rem;
    transition: border-color 0.3s ease;
}
.stTextInput>div>div>input:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

/* Welcome section */
.welcome-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 3rem;
    border-radius: 1.5rem;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
}
</style>
""", unsafe_allow_html=True)

# Supported languages configuration
SUPPORTED_LANGUAGES = {
    "Kiswahili": {
        "code": "sw",
        "name": "Kiswahili",
        "greeting": "Hujambo! Karibu kwenye mfumo wa kujifunza Kiswahili.",
        "description": "Learn Swahili grammar, vocabulary, and sentence construction",
        "tts_lang": "sw"  # Google TTS language code
    },
    "Kikuyu": {
        "code": "ki",
        "name": "Kikuyu",
        "greeting": "Wĩ mwega! Ũkĩrĩte gũkũ kũruta Kikuyu.",
        "description": "Learn Kikuyu grammar, vocabulary, and sentence construction",
        "tts_lang": "en"  # Fallback to English for unsupported languages
    },
    "English": {
        "code": "en",
        "name": "English",
        "greeting": "Welcome! Let's improve your English language skills.",
        "description": "Master English grammar, vocabulary, and communication skills",
        "tts_lang": "en"  # Native English TTS
    }
}

# Voice/Audio helper functions
def text_to_speech(text, lang_code="sw"):
    """Convert text to speech and return audio"""
    try:
        # Create TTS object
        tts = gTTS(text=text, lang=lang_code, slow=False)
        
        # Save to BytesIO object
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        
        return audio_bytes
    except Exception as e:
        st.error(f"Error generating speech: {str(e)}")
        return None

def autoplay_audio(audio_bytes):
    """Auto-play audio in Streamlit"""
    if audio_bytes:
        audio_base64 = base64.b64encode(audio_bytes.read()).decode()
        audio_html = f"""
        <audio autoplay>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)

def create_audio_player(audio_bytes, key=None):
    """Create an audio player widget"""
    if audio_bytes:
        st.audio(audio_bytes, format='audio/mp3')

def speech_to_text_interface():
    """
    Enhanced speech-to-text interface with language-specific recognition and AI correction
    """
    # Get current language
    lang_info = SUPPORTED_LANGUAGES.get(st.session_state.selected_language, SUPPORTED_LANGUAGES["Kiswahili"])
    
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 1.5rem; border-radius: 0.8rem; margin: 1rem 0; color: white;'>
        <h4>🎤 Speech Input ({lang_info['name']})</h4>
        <p>Record your voice in {lang_info['name']} and we'll convert it to text with AI correction</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Language code mapping for Google Speech Recognition
    lang_codes = {
        "Kiswahili": "sw-KE",  # Swahili (Kenya)
        "Kikuyu": "en-KE",     # Fallback to English (Kenya) - better for Kikuyu
        "English": "en-US"     # English (US)
    }
    
    recognition_lang = lang_codes.get(lang_info['name'], "sw-KE")
    
    # Use Streamlit's audio input
    audio_value = st.audio_input(f"🎙️ Click to record in {lang_info['name']}")
    
    if audio_value:
        st.success("✅ Audio recorded! Processing...")
        
        # Save audio to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
            tmp_file.write(audio_value.getvalue())
            audio_path = tmp_file.name
        
        try:
            # Use speech recognition
            import speech_recognition as sr
            recognizer = sr.Recognizer()
            
            # Adjust for ambient noise and energy threshold
            recognizer.energy_threshold = 4000
            recognizer.dynamic_energy_threshold = True
            
            with sr.AudioFile(audio_path) as source:
                # Adjust for ambient noise
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio_data = recognizer.record(source)
                
            # Try to recognize speech with language-specific settings
            try:
                # First attempt: Use language-specific recognition
                text = recognizer.recognize_google(audio_data, language=recognition_lang)
                
                st.info(f"🔊 Raw transcription: **{text}**")
                
                # Second step: Use AI to correct and improve transcription
                with st.spinner("🤖 Using AI to improve transcription..."):
                    llm = initialize_llm()
                    correction_prompt = f"""You are a {lang_info['name']} language expert. 

A speech recognition system transcribed this audio, but it may have errors because it's not optimized for {lang_info['name']}.

Raw transcription: "{text}"
Language: {lang_info['name']}

Your task:
1. Identify likely transcription errors (wrong words, spelling mistakes)
2. Correct them based on {lang_info['name']} language patterns
3. Provide the corrected text

Respond in this format:
CORRECTED: [The corrected text in {lang_info['name']}]
CONFIDENCE: [high/medium/low]
EXPLANATION: [Brief explanation of corrections made, if any]

If the transcription looks correct, just return it as is."""

                    try:
                        response = llm.invoke(correction_prompt)
                        correction_result = response.content
                        
                        # Parse AI response
                        corrected_text = text  # Default to original
                        confidence = "medium"
                        explanation = ""
                        
                        if "CORRECTED:" in correction_result:
                            corrected_text = correction_result.split("CORRECTED:")[1].split("CONFIDENCE:")[0].strip()
                        
                        if "CONFIDENCE:" in correction_result:
                            confidence = correction_result.split("CONFIDENCE:")[1].split("EXPLANATION:")[0].strip()
                        
                        if "EXPLANATION:" in correction_result:
                            explanation = correction_result.split("EXPLANATION:")[1].strip()
                        
                        # Display results
                        st.success(f"✅ **AI-Corrected Text:** {corrected_text}")
                        
                        if explanation:
                            st.info(f"💡 **Corrections made:** {explanation}")
                        
                        # Confidence indicator
                        if confidence.lower() == "high":
                            st.success("🎯 High confidence in transcription")
                        elif confidence.lower() == "medium":
                            st.warning("⚠️ Medium confidence - please verify")
                        else:
                            st.error("❌ Low confidence - please check carefully")
                        
                        # Store corrected text in session state
                        st.session_state.transcribed_text = corrected_text
                        
                        # Show copy button
                        st.markdown(f"""
                        <div style='background: #f0f2f6; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0;'>
                            <p><strong>📋 Copy this text:</strong></p>
                            <p style='font-size: 1.2rem; color: #1f1f1f;'>{corrected_text}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        st.info("💡 Copy the text above and paste it in the question box below!")
                        
                    except Exception as e:
                        st.warning(f"AI correction failed: {str(e)}")
                        st.info(f"Using raw transcription: **{text}**")
                        st.session_state.transcribed_text = text
                
            except sr.UnknownValueError:
                st.error("❌ Could not understand audio. Please try again with:")
                st.markdown("""
                - Speak more clearly and slowly
                - Reduce background noise
                - Speak closer to the microphone
                - Try recording in a quieter environment
                """)
            except sr.RequestError as e:
                st.error(f"❌ Speech recognition service error: {e}")
                st.info("Please check your internet connection and try again.")
                
        except Exception as e:
            st.error(f"Error processing audio: {str(e)}")
            st.info("💡 Make sure you have an internet connection for speech recognition.")
        finally:
            # Clean up temp file
            try:
                os.unlink(audio_path)
            except:
                pass
    else:
        st.info(f"""
        **How to use Speech Input for {lang_info['name']}:**
        
        1. 🎤 Click the microphone button above
        2. 🔴 Allow microphone access if prompted
        3. 🗣️ Speak your question clearly in {lang_info['name']}
        4. ⏹️ Click stop when done
        5. 🤖 AI will transcribe and correct your speech
        6. 📋 Copy the corrected text to the question box
        
        **Tips for better recognition:**
        - Speak clearly and at a moderate pace
        - Minimize background noise
        - Use proper {lang_info['name']} pronunciation
        - Keep recordings under 30 seconds
        
        **Note:** Requires internet connection. AI correction helps fix transcription errors.
        """)
    
    return None

# Initialize session state
if 'selected_language' not in st.session_state:
    st.session_state.selected_language = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_mode' not in st.session_state:
    st.session_state.current_mode = "chat"
if 'quiz_questions' not in st.session_state:
    st.session_state.quiz_questions = []
if 'current_quiz_index' not in st.session_state:
    st.session_state.current_quiz_index = 0
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = []
if 'voice_enabled' not in st.session_state:
    st.session_state.voice_enabled = False
if 'auto_play_responses' not in st.session_state:
    st.session_state.auto_play_responses = False
if 'speech_input_enabled' not in st.session_state:
    st.session_state.speech_input_enabled = False

def load_language_knowledge_from_json(language):
    """Load language knowledge from JSON files"""
    try:
        filename_map = {
            "Kiswahili": "kiswahili_knowledge.json",
            "Kikuyu": "kikuyu_knowledge.json",
            "English": "english_knowledge.json"
        }
        
        if language not in filename_map:
            return None
            
        filepath = os.path.join("language_data", filename_map[language])
        
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Fallback to basic knowledge if file doesn't exist
            return get_fallback_knowledge(language)
    except Exception as e:
        st.error(f"Error loading knowledge for {language}: {str(e)}")
        return get_fallback_knowledge(language)

def get_fallback_knowledge(language):
    """Fallback knowledge base if JSON files are not available"""
    return {
        "language": language,
        "grammar_rules": [
            {"rule": "Basic Grammar", "description": f"Learn {language} grammar patterns", "examples": []}
        ],
        "vocabulary": {
            "basic_words": {
                "hello": {"meaning": "greeting", "pos": "interjection", "examples": ["Hello, how are you?"]}
            }
        },
        "common_errors": [
            {"error": "Common mistakes", "correct": "Learn proper usage", "example": "Practice makes perfect"}
        ],
        "cultural_context": [f"{language} is an important African language with rich cultural heritage"]
    }

def initialize_llm():
    """Initialize the language model with optimized settings"""
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",  # Using fast Flash model
        temperature=0.1,  # Lower temperature for faster, more consistent responses
        max_tokens=500,  # Limit tokens for faster generation
        timeout=10,  # 10 second timeout
        google_api_key=google_api_key  # Explicitly pass API key
    )

def create_language_tutor_prompt():
    """Create specialized prompt for language tutoring"""
    system_prompt = """You are an expert AI tutor for African languages, specializing in {language}. 
    Your role is to help learners improve their grammar, vocabulary, and sentence construction.

    Guidelines:
    1. Provide clear, simple explanations suitable for all learning levels
    2. Give examples in both the target language and English for clarity
    3. Correct mistakes gently and explain why corrections are needed
    4. Encourage use of PURE language without mixing with other languages
       - Teach proper vocabulary in the target language
       - If learners mix languages, gently guide them to use correct terms in the target language
       - Discourage code-switching and promote proper language usage
    5. Be patient with learners while maintaining language purity standards
    6. Provide cultural context when relevant
    7. Generate practice exercises and quizzes when requested
    8. When learners make spelling errors, correct them and show the right spelling

    When analyzing input:
    - For vocabulary: provide meaning, part of speech, usage examples
    - For grammar: explain structure, rules, and common patterns
    - For sentences: check grammar, suggest improvements, offer alternatives
    - For errors: explain mistakes clearly and provide correct versions
    - For typos: identify the intended word and provide correction with explanation

    Always be encouraging and culturally sensitive while maintaining language standards.
    
    Context from knowledge base: {context}
    """
    
    return ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}")
    ])

def load_language_knowledge(language):
    """Load knowledge base for selected language and convert to text"""
    knowledge_data = load_language_knowledge_from_json(language)
    
    if not knowledge_data:
        return ""
    
    # Convert JSON data to text format for embedding
    text_content = f"Language: {language}\n\n"
    
    # Grammar rules
    text_content += "Grammar Rules:\n"
    for rule in knowledge_data.get('grammar_rules', []):
        text_content += f"- {rule.get('rule', '')}: {rule.get('description', '')}\n"
        for example in rule.get('examples', []):
            text_content += f"  Example: {example}\n"
    
    # Vocabulary
    text_content += "\nVocabulary:\n"
    vocab = knowledge_data.get('vocabulary', {})
    
    # Basic words
    for word, info in vocab.get('basic_words', {}).items():
        text_content += f"- {word}: {info.get('meaning', '')} ({info.get('pos', '')})\n"
        for example in info.get('examples', []):
            text_content += f"  Example: {example}\n"
    
    # Greetings
    for greeting, info in vocab.get('greetings', {}).items():
        text_content += f"- {greeting}: {info.get('meaning', '')} (Response: {info.get('response', '')})\n"
        text_content += f"  Usage: {info.get('usage', '')}\n"
    
    # Common errors
    text_content += "\nCommon Errors:\n"
    for error in knowledge_data.get('common_errors', []):
        text_content += f"- Error: {error.get('error', '')}\n"
        text_content += f"  Correct: {error.get('correct', '')}\n"
        text_content += f"  Example: {error.get('example', '')}\n"
    
    # Cultural context
    text_content += "\nCultural Context:\n"
    for context in knowledge_data.get('cultural_context', []):
        text_content += f"- {context}\n"
    
    return text_content

@st.cache_resource
def setup_knowledge_base(language):
    """Setup vector store with language knowledge"""
    knowledge_text = load_language_knowledge(language)
    
    if not knowledge_text:
        return None
    
    try:
        # Create document directly from text instead of using file loader
        doc = Document(page_content=knowledge_text, metadata={"language": language})
        
        # Split the document into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        splits = text_splitter.split_documents([doc])
        
        # Create embeddings and vector store with embedding model
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        vectorstore = FAISS.from_documents(splits, embeddings)
        
        return vectorstore
    except Exception as e:
        st.warning(f"Knowledge base setup issue: {str(e)}. Using direct LLM mode.")
        return None

def generate_quiz_questions(language, num_questions=10):
    """Generate quiz questions dynamically using AI in the target language"""
    try:
        llm = initialize_llm()
        
        # Generate questions in the target language
        quiz_prompt = f"""Generate {num_questions} quiz questions to test {language} language skills.

IMPORTANT RULES:
1. ALL questions must be written IN {language} (not in English)
2. Mix different types: vocabulary, grammar, translation, sentence completion
3. Questions should test real language understanding
4. Vary difficulty from basic to intermediate

Format each question EXACTLY like this:
QUESTION: [Question in {language}]
TYPE: [vocabulary/grammar/translation/sentence]
DIFFICULTY: [easy/medium/hard]
---

Example for Kiswahili:
QUESTION: Neno "nyumba" linamaanisha nini?
TYPE: vocabulary
DIFFICULTY: easy
---

Generate {num_questions} unique questions now:"""

        response = llm.invoke(quiz_prompt)
        questions_text = response.content
        
        # Parse questions
        questions = []
        question_blocks = questions_text.split("---")
        
        for block in question_blocks:
            if "QUESTION:" in block:
                try:
                    question_text = block.split("QUESTION:")[1].split("TYPE:")[0].strip()
                    question_type = block.split("TYPE:")[1].split("DIFFICULTY:")[0].strip()
                    difficulty = block.split("DIFFICULTY:")[1].strip().split("\n")[0].strip()
                    
                    questions.append({
                        "question": question_text,
                        "category": question_type,
                        "difficulty": difficulty,
                        "language": language
                    })
                except:
                    continue
        
        # If parsing failed, create fallback questions
        if len(questions) < 5:
            questions = generate_fallback_questions(language)
        
        return questions[:num_questions]
    
    except Exception as e:
        st.error(f"Error generating quiz: {str(e)}")
        return generate_fallback_questions(language)

def generate_fallback_questions(language):
    """Fallback questions if AI generation fails"""
    fallback = {
        "Kiswahili": [
            {"question": "Neno 'mtu' linamaanisha nini?", "category": "vocabulary", "difficulty": "easy", "language": language},
            {"question": "Tafsiri 'nyumba' kwa Kiingereza", "category": "translation", "difficulty": "easy", "language": language},
            {"question": "Kamilisha sentensi: 'Mimi ____ kitabu' (ninasoma)", "category": "grammar", "difficulty": "medium", "language": language},
            {"question": "Nini wingi wa 'kitabu'?", "category": "grammar", "difficulty": "easy", "language": language},
            {"question": "Andika sentensi kwa wakati uliopita: 'Ninasoma'", "category": "grammar", "difficulty": "medium", "language": language},
        ],
        "Kikuyu": [
            {"question": "Nĩ ũndũ ũrĩkũ 'mũndũ' ũrĩ?", "category": "vocabulary", "difficulty": "easy", "language": language},
            {"question": "Tafsiri 'nyũmba' kwa Kiingereza", "category": "translation", "difficulty": "easy", "language": language},
            {"question": "Kamilisha: 'Nĩ ____ mũrutani' (ndĩ)", "category": "grammar", "difficulty": "medium", "language": language},
            {"question": "Nĩ ũrĩkũ wingi wa 'mũndũ'?", "category": "grammar", "difficulty": "easy", "language": language},
            {"question": "Andika 'gũthoma' kwa wakati ũrĩa ũhĩtũkĩte", "category": "grammar", "difficulty": "medium", "language": language},
        ],
        "English": [
            {"question": "What is the past tense of 'go'?", "category": "grammar", "difficulty": "easy", "language": language},
            {"question": "Complete: 'She ___ to school every day' (goes/go)", "category": "grammar", "difficulty": "easy", "language": language},
            {"question": "What is the plural of 'child'?", "category": "vocabulary", "difficulty": "easy", "language": language},
            {"question": "Choose the correct article: '___ apple' (a/an)", "category": "grammar", "difficulty": "easy", "language": language},
            {"question": "What does 'beautiful' mean?", "category": "vocabulary", "difficulty": "easy", "language": language},
        ]
    }
    
    return fallback.get(language, fallback["English"])

def main():
    # Header
    st.markdown("<h1 class='main-header'>🌍 African Language AI Tutor</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Master African languages with AI-powered personalized tutoring</p>", unsafe_allow_html=True)
    
    # Language selection
    if not st.session_state.selected_language:
        # Welcome section
        st.markdown("""
        <div class='welcome-section'>
            <h2>🌍 Welcome to Your Language Learning Journey!</h2>
            <p style='font-size: 1.2rem; margin-top: 1rem;'>
                Choose your language and start mastering African languages with AI-powered tutoring
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 🗣️ Choose Your Language")
        
        # Create 2x2 grid for language cards
        cols = st.columns(2)
        for i, (lang_code, lang_info) in enumerate(SUPPORTED_LANGUAGES.items()):
            col = cols[i % 2]
            with col:
                # Create clickable card with button
                if st.button(
                    f"🌟 {lang_info['name']}", 
                    key=f"lang_{lang_code}", 
                    use_container_width=True,
                    help=f"Start learning {lang_info['name']}"
                ):
                    st.session_state.selected_language = lang_code
                    st.session_state.chat_history = []
                    st.rerun()
                
                # Display language card info
                st.markdown(f"""
                <div class='language-card'>
                    <h3>{lang_info['name']}</h3>
                    <p style='font-style: italic; margin: 0.5rem 0;'>"{lang_info['greeting']}"</p>
                    <p>{lang_info['description']}</p>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Features overview with enhanced styling
        st.markdown("### 🎯 What You'll Learn")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            <div class='feature-box'>
                <h4>📚 Vocabulary Building</h4>
                <p>Learn new words with meanings, pronunciation, and usage examples in context</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='feature-box'>
                <h4>📝 Grammar Mastery</h4>
                <p>Understand sentence structure, verb conjugations, and language rules</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class='feature-box'>
                <h4>🎮 Interactive Practice</h4>
                <p>Quizzes, exercises, and conversational practice with instant feedback</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Additional features
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### ✨ Special Features")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class='feature-box'>
                <h4>🎤 Voice Support</h4>
                <p>Text-to-speech for pronunciation practice</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='feature-box'>
                <h4>🌍 Cultural Context</h4>
                <p>Learn proper usage and cultural significance</p>
            </div>
            """, unsafe_allow_html=True)
        
        return
    
    # Main interface for selected language
    selected_lang_info = SUPPORTED_LANGUAGES[st.session_state.selected_language]
    
    # Sidebar
    with st.sidebar:
        st.markdown(f"### 🗣️ {selected_lang_info['name']} Tutor")
        
        if st.button("🔄 Change Language"):
            st.session_state.selected_language = None
            st.session_state.chat_history = []
            st.rerun()
        
        st.markdown("---")
        
        # Voice settings
        st.markdown("### 🎤 Voice Settings")
        st.session_state.voice_enabled = st.checkbox(
            "Enable Voice Output (TTS)",
            value=st.session_state.voice_enabled,
            help="Enable text-to-speech for responses"
        )
        
        if st.session_state.voice_enabled:
            st.session_state.auto_play_responses = st.checkbox(
                "Auto-play Responses",
                value=st.session_state.auto_play_responses,
                help="Automatically play audio for AI responses"
            )
        
        st.session_state.speech_input_enabled = st.checkbox(
            "Enable Speech Input (STT)",
            value=st.session_state.speech_input_enabled,
            help="Enable speech-to-text for questions"
        )
        
        st.markdown("---")
        
        # Mode selection
        st.markdown("### 📚 Learning Mode")
        mode = st.radio(
            "Choose mode:",
            ["💬 Chat Tutor", "🎯 Quiz Practice", "📖 Vocabulary Builder"],
            key="mode_selector"
        )
        
        if mode == "💬 Chat Tutor":
            st.session_state.current_mode = "chat"
        elif mode == "🎯 Quiz Practice":
            st.session_state.current_mode = "quiz"
        else:
            st.session_state.current_mode = "vocabulary"
        
        st.markdown("---")
        
        # Quick help
        st.markdown("### 💡 Quick Tips")
        st.info(f"""
        **Ask me about:**
        - Word meanings and usage
        - Grammar rules and structure
        - Sentence corrections
        - Cultural context
        - Practice exercises
        
        **Example:** "What does 'nyumba' mean?" or "How do I say 'I am learning' in {selected_lang_info['name']}?"
        """)
        
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Main content area
    if st.session_state.current_mode == "chat":
        show_chat_interface(selected_lang_info)
    elif st.session_state.current_mode == "quiz":
        show_quiz_interface(selected_lang_info)
    else:
        show_vocabulary_interface(selected_lang_info)

def show_chat_interface(lang_info):
    """Display the main chat interface"""
    # Enhanced header with gradient background
    st.markdown(f"""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 1rem; margin-bottom: 2rem; color: white;'>
        <h2 style='margin: 0; text-align: center;'>💬 Chat with your {lang_info['name']} tutor</h2>
        <p style='text-align: center; font-style: italic; margin-top: 0.5rem; font-size: 1.1rem;'>
            {lang_info['greeting']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add voice greeting button
    if st.session_state.voice_enabled:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔊 Play Greeting", use_container_width=True):
                audio = text_to_speech(lang_info['greeting'], lang_info['tts_lang'])
                if audio:
                    create_audio_player(audio, key="greeting_audio")
    
    # Setup knowledge base and LLM
    vectorstore = setup_knowledge_base(st.session_state.selected_language)
    llm = initialize_llm()
    
    # Display chat history with enhanced styling
    if st.session_state.chat_history:
        st.markdown("### 💭 Conversation")
    
    for i, message in enumerate(st.session_state.chat_history):
        if message["role"] == "user":
            st.markdown(f"""
            <div class="chat-message user">
                <strong>👤 You:</strong><br>
                <span style='font-size: 1.1rem; margin-top: 0.5rem; display: block;'>{message["content"]}</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant">
                <strong>🤖 Tutor:</strong><br>
                <span style='font-size: 1.1rem; margin-top: 0.5rem; display: block;'>{message["content"]}</span>
            </div>
            """, unsafe_allow_html=True)
            
            # Add audio player for each response if voice is enabled
            if st.session_state.voice_enabled:
                col1, col2, col3, col4 = st.columns([3, 1, 1, 3])
                with col2:
                    if st.button(f"🔊 Play", key=f"play_response_{i}"):
                        audio = text_to_speech(message["content"], lang_info['tts_lang'])
                        if audio:
                            create_audio_player(audio, key=f"response_audio_{i}")
    
    # Chat input with enhanced styling
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### ✍️ Your Question")
    
    # Speech input option
    if st.session_state.speech_input_enabled:
        speech_to_text_interface()
        st.markdown("<br>", unsafe_allow_html=True)
    
    with st.form("chat_form", clear_on_submit=True):
        # Pre-fill with transcribed text if available
        default_text = st.session_state.get('transcribed_text', '')
        
        user_input = st.text_input(
            "Type your question here:",
            value=default_text,
            placeholder=f"e.g., 'How do I say hello in {lang_info['name']}?' or 'Check this sentence: Mimi ninasoma'",
            label_visibility="collapsed"
        )
        
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            submit = st.form_submit_button("Send 📤", use_container_width=True)
        
        if submit and user_input:
            # Clear transcribed text after using it
            if 'transcribed_text' in st.session_state:
                del st.session_state.transcribed_text
            handle_chat_query(user_input, vectorstore, llm, lang_info)

def handle_chat_query(query, vectorstore, llm, lang_info):
    """Process chat query and generate response"""
    st.session_state.chat_history.append({"role": "user", "content": query})
    
    with st.spinner("🤔 Thinking..."):
        try:
            # Create prompt template
            prompt_template = create_language_tutor_prompt()
            
            # Retrieve relevant context if vectorstore available
            context = ""
            if vectorstore:
                retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
                docs = retriever.get_relevant_documents(query)
                context = "\n\n".join([doc.page_content for doc in docs])
            
            # Format prompt with context
            formatted_prompt = prompt_template.format_messages(
                language=lang_info['name'],
                context=context if context else "No specific context available.",
                input=query
            )
            # Generate response
            response = llm.invoke(formatted_prompt)
            answer = response.content
            
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            
            # Auto-play response if enabled
            if st.session_state.voice_enabled and st.session_state.auto_play_responses:
                audio = text_to_speech(answer, lang_info['tts_lang'])
                if audio:
                    autoplay_audio(audio)
            
            st.rerun()
            
        except Exception as e:
            st.error(f"Sorry, I encountered an error: {str(e)}")

def show_quiz_interface(lang_info):
    """Display quiz practice interface with scoring"""
    st.markdown(f"### 🎯 {lang_info['name']} Quiz Practice")
    
    if not st.session_state.quiz_questions:
        st.markdown(f"""
        <div class='feature-box'>
            <h4>📝 Ready to test your {lang_info['name']} skills?</h4>
            <p>Get 10 AI-generated questions in {lang_info['name']} to test your knowledge!</p>
            <ul>
                <li>Questions are in {lang_info['name']}</li>
                <li>Mix of vocabulary, grammar, and translation</li>
                <li>Instant feedback with detailed explanations</li>
                <li>Pass with 60% or higher</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎲 Generate New Quiz (10 Questions)", use_container_width=True):
            with st.spinner(f"🤖 Generating {lang_info['name']} quiz questions..."):
                st.session_state.quiz_questions = generate_quiz_questions(lang_info['name'], num_questions=10)
                st.session_state.current_quiz_index = 0
                st.session_state.quiz_score = 0
                st.session_state.quiz_answers = []
            st.rerun()
        
        return
    
    # Display current question
    if st.session_state.current_quiz_index < len(st.session_state.quiz_questions):
        current_q = st.session_state.quiz_questions[st.session_state.current_quiz_index]
        
        # Progress bar
        progress = (st.session_state.current_quiz_index) / len(st.session_state.quiz_questions)
        st.progress(progress)
        
        st.markdown(f"""
        <div class='quiz-question'>
            <h4>Question {st.session_state.current_quiz_index + 1} of {len(st.session_state.quiz_questions)}</h4>
            <p style='font-size: 1.3rem;'><strong>{current_q['question']}</strong></p>
            <small>📂 Type: {current_q['category'].title()} | 🎯 Difficulty: {current_q.get('difficulty', 'medium').title()}</small>
        </div>
        """, unsafe_allow_html=True)
        
        # Answer input
        user_answer = st.text_area(
            "Your answer:", 
            key=f"quiz_answer_{st.session_state.current_quiz_index}",
            placeholder=f"Type your answer in {lang_info['name']} or English...",
            height=100
        )
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Submit Answer", use_container_width=True):
                if user_answer:
                    with st.spinner("🤔 Evaluating your answer..."):
                        # Evaluate answer using LLM with detailed explanation IN THE TARGET LANGUAGE
                        llm = initialize_llm()
                        evaluation_prompt = f"""You are evaluating a {lang_info['name']} language quiz answer.

Question: {current_q['question']}
Student's Answer: {user_answer}
Language: {lang_info['name']}

CRITICAL INSTRUCTION: Provide ALL explanations, feedback, and teaching points IN {lang_info['name']} language (not in English).

Evaluate the answer and respond in this EXACT format:

CORRECT: [yes or no]

EXPLANATION: [2-3 sentences IN {lang_info['name']} explaining why the answer is correct or incorrect. Be specific and educational. ALWAYS provide a clear explanation IN {lang_info['name']}.]

CORRECT_ANSWER: [If wrong, provide the correct answer IN {lang_info['name']}. If correct, restate their answer IN {lang_info['name']}.]

TEACHING_POINT: [One key learning point IN {lang_info['name']} from this question]

Example for Kiswahili:
CORRECT: no
EXPLANATION: Jibu lako si sahihi. Neno 'nakula' linamaanisha 'I am eating' kwa Kiingereza, sio 'I eat'. Wakati wa sasa unaendelea unatumia 'na-' kabla ya mzizi wa kitenzi.
CORRECT_ANSWER: Nakula
TEACHING_POINT: Wakati wa sasa unaendelea unatumia kiambishi 'na-' (mimi nakula, wewe unakula)

Be encouraging and educational. Write EVERYTHING in {lang_info['name']}!"""
                        
                        try:
                            response = llm.invoke(evaluation_prompt)
                            evaluation = response.content
                            
                            # Parse evaluation more robustly
                            is_correct = False
                            explanation = "Jaribu tena!" if lang_info['name'] == "Kiswahili" else "Try again!" if lang_info['name'] == "English" else "Geria rĩngĩ!"
                            correct_answer = ""
                            teaching_point = ""
                            
                            try:
                                if "CORRECT:" in evaluation:
                                    correct_line = evaluation.split("CORRECT:")[1].split("\n")[0].strip().lower()
                                    is_correct = "yes" in correct_line
                                
                                if "EXPLANATION:" in evaluation:
                                    explanation = evaluation.split("EXPLANATION:")[1].split("CORRECT_ANSWER:")[0].strip()
                                
                                if "CORRECT_ANSWER:" in evaluation:
                                    correct_answer = evaluation.split("CORRECT_ANSWER:")[1].split("TEACHING_POINT:")[0].strip()
                                
                                if "TEACHING_POINT:" in evaluation:
                                    teaching_point = evaluation.split("TEACHING_POINT:")[1].strip()
                            except:
                                # Fallback if parsing fails
                                explanation = evaluation
                            
                            # Store answer
                            st.session_state.quiz_answers.append({
                                "question": current_q['question'],
                                "user_answer": user_answer,
                                "correct": is_correct,
                                "explanation": explanation,
                                "correct_answer": correct_answer,
                                "teaching_point": teaching_point
                            })
                            
                            # Language-specific feedback messages
                            success_messages = {
                                "Kiswahili": "✅ Sahihi! Umefanya vizuri!",
                                "Kikuyu": "✅ Nĩ wega! Wĩkĩte wega mũno!",
                                "English": "✅ Correct! Excellent work!"
                            }
                            
                            error_messages = {
                                "Kiswahili": "❌ Si sahihi kabisa. Hebu tujifunze kutoka hapa:",
                                "Kikuyu": "❌ Ti wega. Reke twĩrute kuuma haha:",
                                "English": "❌ Not quite right. Let's learn from this:"
                            }
                            
                            explanation_headers = {
                                "Kiswahili": "📚 Maelezo:",
                                "Kikuyu": "📚 Ũhoro:",
                                "English": "📚 Explanation:"
                            }
                            
                            correct_answer_headers = {
                                "Kiswahili": "✓ Jibu Sahihi:",
                                "Kikuyu": "✓ Macokio Marĩa Mega:",
                                "English": "✓ Correct Answer:"
                            }
                            
                            learning_headers = {
                                "Kiswahili": "💡 Somo Muhimu:",
                                "Kikuyu": "💡 Ũrutani Wa Bata:",
                                "English": "💡 Key Learning:"
                            }
                            
                            if is_correct:
                                st.session_state.quiz_score += 1
                                st.success(success_messages.get(lang_info['name'], success_messages["English"]))
                            else:
                                st.error(error_messages.get(lang_info['name'], error_messages["English"]))
                            
                            # Show detailed feedback
                            st.markdown(f"""
                            <div class='{"feature-box" if is_correct else "correction-box"}'>
                                <h4>{explanation_headers.get(lang_info['name'], explanation_headers["English"])}</h4>
                                <p>{explanation}</p>
                                
                                {f"<h4>{correct_answer_headers.get(lang_info['name'], correct_answer_headers['English'])}</h4><p><strong>{correct_answer}</strong></p>" if correct_answer else ""}
                                
                                {f"<h4>{learning_headers.get(lang_info['name'], learning_headers['English'])}</h4><p>{teaching_point}</p>" if teaching_point else ""}
                            </div>
                            """, unsafe_allow_html=True)
                            
                            # Language-specific button text
                            next_button_text = {
                                "Kiswahili": "➡️ Swali Linalofuata",
                                "Kikuyu": "➡️ Kĩũria Kĩrĩa Kĩngĩ",
                                "English": "➡️ Next Question"
                            }
                            
                            # Auto-advance after showing feedback
                            if st.button(next_button_text.get(lang_info['name'], next_button_text["English"]), use_container_width=True):
                                st.session_state.current_quiz_index += 1
                                st.rerun()
                            
                        except Exception as e:
                            st.error(f"Error evaluating answer: {str(e)}")
                else:
                    st.warning("Please enter an answer before submitting!")
        
        with col2:
            if st.button("⏭️ Skip Question", use_container_width=True):
                st.session_state.quiz_answers.append({
                    "question": current_q['question'],
                    "user_answer": "Skipped",
                    "correct": False,
                    "explanation": "You skipped this question. Try to answer all questions to improve your score!",
                    "correct_answer": "N/A",
                    "teaching_point": "Practice makes perfect!"
                })
                st.session_state.current_quiz_index += 1
                st.rerun()
        
        with col3:
            if st.button("🔄 New Quiz", use_container_width=True):
                st.session_state.quiz_questions = []
                st.session_state.current_quiz_index = 0
                st.session_state.quiz_score = 0
                st.session_state.quiz_answers = []
                st.rerun()
    
    else:
        # Quiz completed - show results
        total_questions = len(st.session_state.quiz_questions)
        score = st.session_state.quiz_score
        percentage = (score / total_questions) * 100
        
        # Determine pass/fail
        passed = percentage >= 60  # 60% passing grade
        
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, {"#4CAF50" if passed else "#f44336"} 0%, {"#8BC34A" if passed else "#e57373"} 100%);
                    padding: 2rem; border-radius: 1rem; color: white; text-align: center; margin: 2rem 0;'>
            <h2>{'🎉 Congratulations! You Passed!' if passed else '📚 Keep Practicing!'}</h2>
            <h1 style='font-size: 3rem; margin: 1rem 0;'>{score}/{total_questions}</h1>
            <h3>{percentage:.1f}%</h3>
            <p style='font-size: 1.2rem; margin-top: 1rem;'>
                {'Excellent work! You have a strong understanding.' if percentage >= 80 
                 else 'Good job! You passed the quiz.' if passed 
                 else "Don't worry! Review the material and try again."}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show detailed results
        st.markdown("### 📊 Detailed Review")
        
        for i, answer in enumerate(st.session_state.quiz_answers, 1):
            status = "✅" if answer['correct'] else "❌"
            st.markdown(f"""
            <div class='{"feature-box" if answer["correct"] else "correction-box"}'>
                <h4>{status} Question {i}: {answer['question']}</h4>
                <p><strong>Your Answer:</strong> {answer['user_answer']}</p>
                <p><strong>Explanation:</strong> {answer.get('explanation', 'Good attempt!')}</p>
                {f"<p><strong>Correct Answer:</strong> {answer.get('correct_answer', '')}</p>" if answer.get('correct_answer') else ""}
                {f"<p><strong>💡 Learning Point:</strong> {answer.get('teaching_point', '')}</p>" if answer.get('teaching_point') else ""}
            </div>
            """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Take New Quiz (Different Questions)", use_container_width=True):
                st.session_state.quiz_questions = []
                st.session_state.current_quiz_index = 0
                st.session_state.quiz_score = 0
                st.session_state.quiz_answers = []
                st.rerun()
        
        with col2:
            if st.button("📚 Back to Learning", use_container_width=True):
                st.session_state.current_mode = "chat"
                st.rerun()

def show_vocabulary_interface(lang_info):
    """Display vocabulary building interface with AI-powered search"""
    st.markdown(f"### 📖 {lang_info['name']} Vocabulary Builder")
    
    # Search vocabulary - AI-powered for ANY word
    search_term = st.text_area(
        "🔍 Search for ANY word or sentence:", 
        placeholder=f"Enter any word, phrase, or sentence in English or {lang_info['name']}\nExample: 'What does beautiful mean?' or 'How do I say computer?'",
        height=100
    )
    
    if search_term:
        st.info("🤖 Using AI to search for your query...")
        
        # Use AI to answer ANY vocabulary question
        with st.spinner("🔍 Searching..."):
            try:
                # Initialize LLM
                llm = initialize_llm()
                
                # Create AI prompt for vocabulary search
                vocab_prompt = f"""You are a {lang_info['name']} language expert. Answer this vocabulary question:

Question: {search_term}

Provide a comprehensive answer including:
1. The word/phrase in {lang_info['name']}
2. Meaning in English
3. Part of speech (noun, verb, adjective, etc.)
4. Pronunciation guide if applicable
5. At least 2-3 example sentences in {lang_info['name']} with English translations
6. Any cultural context or usage notes
7. Related words or synonyms

If the user made a spelling error, correct it and provide the right word.
If asking about multiple words, provide information for each.

Format your response clearly with sections."""

                response = llm.invoke(vocab_prompt)
                answer = response.content
                
                # Display AI response
                st.success(f"✅ Found information for: '{search_term}'")
                
                st.markdown(f"""
                <div class='feature-box'>
                    {answer.replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)
                
                # Add audio button if voice enabled
                if st.session_state.voice_enabled:
                    st.markdown("---")
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        if st.button(f"🔊 Hear pronunciation", key=f"vocab_audio_btn", use_container_width=True):
                            # Extract the main word from the response for pronunciation
                            audio = text_to_speech(search_term, lang_info['tts_lang'])
                            if audio:
                                create_audio_player(audio, key=f"vocab_audio_player")
                
            except Exception as e:
                st.error(f"Error searching: {str(e)}")
                st.info("Try rephrasing your question or check your internet connection.")
    else:
        # Show helpful examples when no search
        st.info(f"""💡 **Try asking:**
        - "What does 'beautiful' mean in {lang_info['name']}?"
        - "How do I say 'computer' in {lang_info['name']}?"
        - "What is the word for 'family'?"
        - "Translate 'I love you' to {lang_info['name']}"
        - Any word you want to learn!
        """)
    
    st.markdown("---")
    
    # Quick access to common categories
    st.markdown("### 📚 Quick Category Search")
    st.caption("Click a category to get common words in that area")
    
    categories = {
        "Family": "family members like mother, father, sister, brother",
        "Food": "common foods and meals",
        "Colors": "all color names",
        "Numbers": "numbers 1-20",
        "Greetings": "common greetings and responses",
        "Time": "days, months, time expressions",
        "Animals": "common animals",
        "Body Parts": "parts of the body"
    }
    
    cols = st.columns(4)
    for i, (category, description) in enumerate(categories.items()):
        col = cols[i % 4]
        with col:
            if st.button(f"📂 {category}", use_container_width=True, key=f"cat_{category}"):
                # Use AI to generate vocabulary for this category
                with st.spinner(f"Loading {category} vocabulary..."):
                    try:
                        llm = initialize_llm()
                        category_prompt = f"""List 10-15 common {description} in {lang_info['name']} with English translations.

Format each entry as:
- {lang_info['name']} word (English meaning)

Example:
- mtu (person)
- nyumba (house)

Provide clear, accurate translations."""

                        response = llm.invoke(category_prompt)
                        st.markdown(f"""
                        <div class='feature-box'>
                            <h4>📂 {category} Vocabulary</h4>
                            {response.content.replace(chr(10), '<br>')}
                        </div>
                        """, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error loading category: {str(e)}")

if __name__ == "__main__":
    main()