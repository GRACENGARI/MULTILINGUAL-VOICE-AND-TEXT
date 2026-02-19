import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
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
openai_api_key = None

# 1. Try Streamlit secrets (for Streamlit Cloud deployment)
try:
    openai_api_key = st.secrets["OPENAI_API_KEY"]
except:
    pass

# 2. Try environment variable (for local development and other platforms)
if not openai_api_key:
    openai_api_key = os.getenv("OPENAI_API_KEY")

# Check if API key is loaded (without displaying it)
if not openai_api_key:
    st.sidebar.error("❌ OpenAI API Key not found! Please check your .env file or Streamlit secrets.")


if not openai_api_key:
    st.error("⚠️ OPENAI_API_KEY is not set. Please check your .env file.")
    st.info("""
    **To fix this:**
    1. Make sure .env file exists in the project root
    2. Add this line: OPENAI_API_KEY=your_actual_key_here
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

# Gĩkũyũ Dictionary - Verified vocabulary to prevent hallucinations
GIKUYU_DICTIONARY = {
    "nouns": {
        "mũndũ": "person (singular)",
        "andũ": "people (plural)",
        "mũtĩ": "tree",
        "mĩtĩ": "trees",
        "mwana": "child",
        "ciana": "children",
        "njũĩ": "river",
        "nyũmba": "house",
        "ng'ombe": "cow",
        "mbũri": "goat",
        "ũhoro": "news/information/matter"
    },
    "verbs": {
        "gũthoma": "to read / to study",
        "kũrĩa": "to eat",
        "kũnyua": "to drink",
        "gũthiĩ": "to go",
        "kwaria": "to speak",
        "kũina": "to sing / to dance",
        "kũruga": "to cook",
        "gũkenera": "to enjoy / be happy"
    },
    "greetings_phrases": {
        "ũhoro waku": "how are you? (singular)",
        "ũhoro wanyu": "how are you? (plural)",
        "nĩ wega": "thank you / it is good",
        "nuu": "who",
        "kĩĩ": "what",
        "atĩa": "how"
    },
    "numbers": {
        "ĩmwe": "1",
        "igĩrĩ": "2",
        "ithatũ": "3",
        "inya": "4",
        "ithano": "5",
        "mũgwanja": "7",
        "nyanya": "8",
        "kenda": "9",
        "ikũmi": "10"
    }
}

# Hallucination Blacklist - Swahili words that GPT-4 incorrectly uses for Gĩkũyũ
GIKUYU_HALLUCINATION_BLACKLIST = {
    "habari": {"correct": "ũhoro", "note": "AI often uses Swahili 'habari' instead of Gĩkũyũ 'ũhoro'"},
    "mti": {"correct": "mũtĩ", "note": "Missing tilde (ũ) - this is Swahili, not Gĩkũyũ"},
    "kula": {"correct": "kũrĩa", "note": "AI defaults to Swahili 'kula' instead of Gĩkũyũ 'kũrĩa'"},
    "asante": {"correct": "nĩ wega", "note": "Common greeting hallucination - use Gĩkũyũ 'nĩ wega'"},
    "watoto": {"correct": "ciana", "note": "Use Gĩkũyũ 'ciana' for plural 'children'"},
    "nyumba": {"correct": "nyũmba", "note": "Missing tilde - ensure proper Gĩkũyũ spelling"},
    "chakula": {"correct": "irĩo", "note": "Swahili word - use Gĩkũyũ 'irĩo' for food"},
    "maji": {"correct": "maaĩ", "note": "Use Gĩkũyũ 'maaĩ' with proper diacritics"},
    "kwenda": {"correct": "gũthiĩ", "note": "Swahili verb - use Gĩkũyũ 'gũthiĩ'"},
    "kusoma": {"correct": "gũthoma", "note": "Swahili infinitive - use Gĩkũyũ 'gũthoma'"}
}

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
        "tts_lang": "sw"  # Use Swahili TTS as closest available for Kikuyu
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
    
    # Disable speech input for Kikuyu (not supported by Google Speech Recognition)
    if lang_info['name'] == "Kikuyu":
        st.warning("⚠️ Speech input is not available for Kikuyu")
        st.info("""
        **Why?** Google's speech recognition doesn't support Kikuyu language yet. 
        
        Please type your questions instead. We're working on adding Kikuyu speech support in the future.
        """)
        return
    
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

def detect_gikuyu_hallucinations(text):
    """
    Detect Swahili/Sheng hallucinations in Gĩkũyũ responses
    Returns: (has_hallucinations, corrections_list)
    """
    if not text:
        return False, []
    
    text_lower = text.lower()
    corrections = []
    
    # Check for blacklisted Swahili words
    for swahili_word, correction_info in GIKUYU_HALLUCINATION_BLACKLIST.items():
        # Use word boundaries to avoid partial matches
        import re
        pattern = r'\b' + re.escape(swahili_word) + r'\b'
        if re.search(pattern, text_lower):
            corrections.append({
                "error": swahili_word,
                "correct": correction_info["correct"],
                "note": correction_info["note"]
            })
    
    return len(corrections) > 0, corrections

def validate_gikuyu_response(response_text, lang_info):
    """
    Validate Gĩkũyũ responses and correct hallucinations
    """
    if lang_info['name'] != "Kikuyu":
        return response_text, False, []
    
    has_errors, corrections = detect_gikuyu_hallucinations(response_text)
    
    if has_errors:
        # Create correction message
        corrected_text = response_text
        for correction in corrections:
            import re
            pattern = r'\b' + re.escape(correction["error"]) + r'\b'
            corrected_text = re.sub(pattern, correction["correct"], corrected_text, flags=re.IGNORECASE)
        
        return corrected_text, True, corrections
    
    return response_text, False, []

def initialize_llm():
    """Initialize GPT-4 with minimal temperature to maximize factual accuracy"""
    return ChatOpenAI(
        model="gpt-4",  # GPT-4 has much better knowledge of African languages
        temperature=0.0,  # Zero temperature for maximum factual accuracy and minimal hallucination
        max_tokens=500,  # Limit tokens for faster generation
        timeout=30,  # 30 second timeout for GPT-4
        openai_api_key=openai_api_key  # Explicitly pass API key
    )

def create_language_tutor_prompt():
    """Create specialized prompt leveraging GPT-4's strong multilingual capabilities"""
    system_prompt = """You are an expert AI tutor for African languages, specializing in {language}. 
    You are powered by GPT-4 and have strong knowledge of African languages.

    Your role is to help learners master {language} through clear, accurate instruction.

    CRITICAL - ANTI-HALLUCINATION RULES FOR GĨKŨYŨ:
    If teaching Gĩkũyũ (Kikuyu), you MUST follow these STRICT rules:
    
    1. NEVER EVER use Swahili words when teaching Gĩkũyũ - this is the #1 error to avoid:
       - BANNED: "habari" → ONLY USE: "ũhoro" (news/how are you)
       - BANNED: "mti" → ONLY USE: "mũtĩ" (tree - note the tilde ũ)
       - BANNED: "kula" → ONLY USE: "kũrĩa" (to eat)
       - BANNED: "asante" → ONLY USE: "nĩ wega" (thank you)
       - BANNED: "watoto" → ONLY USE: "ciana" (children)
       - BANNED: "chakula" → ONLY USE: "irĩo" (food)
       - BANNED: "maji" → ONLY USE: "maaĩ" (water)
       - BANNED: "kwenda" → ONLY USE: "gũthiĩ" (to go)
       - BANNED: "kusoma" → ONLY USE: "gũthoma" (to read)
       - BANNED: "nyumba" → ONLY USE: "nyũmba" (house - with tilde)
    
    2. ALWAYS use proper Gĩkũyũ diacritics - they are NOT optional:
       - ũ, ĩ, ĩ are REQUIRED - never omit them
       - Example: "mũndũ" NOT "mundu"
       - Example: "mũtĩ" NOT "mti"
    
    3. ONLY use vocabulary from the verified knowledge base provided
    
    4. If you don't know a Gĩkũyũ word, say "I'm not certain of the exact Gĩkũyũ word" - DO NOT guess or use Swahili
    
    5. Before responding, ask yourself: "Does this word sound like Swahili?" If YES, find the Gĩkũyũ equivalent
    
    6. DOUBLE-CHECK every word - Swahili contamination is the most common error

    TEACHING APPROACH:
    1. Provide accurate, helpful answers to all language questions
    2. Give clear explanations with practical examples
    3. Teach proper vocabulary, grammar, and pronunciation
    4. Encourage pure language usage without code-switching
    5. Correct mistakes gently with clear explanations
    6. Provide cultural context and usage notes
    7. Be encouraging and supportive

    When responding:
    - For vocabulary: provide meaning, part of speech, pronunciation, and usage examples
    - For grammar: explain structure, rules, and patterns with clear examples
    - For sentences: analyze grammar and suggest improvements
    - For translations: provide accurate translations with context
    - Be conversational, educational, and accurate

    Knowledge base context: {context}
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
        
        # Create embeddings and vector store with OpenAI embedding model
        embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        vectorstore = FAISS.from_documents(splits, embeddings)
        
        return vectorstore
    except Exception as e:
        st.warning(f"Knowledge base setup issue: {str(e)}. Using direct LLM mode.")
        return None

def generate_quiz_questions(language, num_questions=5):
    """Generate reliable quiz questions from predefined set to prevent hallucinations"""
    # Use predefined questions instead of AI generation to prevent hallucinations
    # Start with 5 questions, then generate 5 more after completion
    return generate_fallback_questions(language)[:num_questions]

def generate_fallback_questions(language):
    """Curated, verified questions for each language"""
    fallback = {
        "Kiswahili": [
            {
                "id": 1,
                "question": "-----amelia sana (Mtoto/Kitoto)",
                "category": "Grammar",
                "difficulty": "easy",
                "language": language,
                "correct_answer": "mtoto",
                "acceptable_answers": ["mtoto"]
            },
            {
                "id": 2,
                "question": "Kamilisha sentensi: 'Mimi ____ kitabu' (soma)",
                "category": "Grammar",
                "difficulty": "medium",
                "language": language,
                "correct_answer": "nasoma",
                "acceptable_answers": ["nasoma", "ninasoma"]
            },
            {
                "id": 3,
                "question": "Tafsiri 'nyumba' kwa Kiingereza",
                "category": "Translation",
                "difficulty": "easy",
                "language": language,
                "correct_answer": "house",
                "acceptable_answers": ["house", "home"]
            },
            {
                "id": 4,
                "question": "Wingi wa kitabu ni",
                "category": "Grammar",
                "difficulty": "easy",
                "language": language,
                "correct_answer": "vitabu",
                "acceptable_answers": ["vitabu"]
            },
            {
                "id": 5,
                "question": "Tafsiri 'I am eating' kwa Kiswahili",
                "category": "Translation",
                "difficulty": "medium",
                "language": language,
                "correct_answer": "ninakula",
                "acceptable_answers": ["ninakula", "nakula"]
            },
            {
                "id": 6,
                "question": "Kamilisha: 'Wewe ____ wapi?' (enda)",
                "category": "Grammar",
                "difficulty": "medium",
                "language": language,
                "correct_answer": "unaenda",
                "acceptable_answers": ["unaenda", "unakwenda"]
            },
            {
                "id": 7,
                "question": "mzee ---- mkoba (amebeba/amebebwa)",
                "category": "Grammar",
                "difficulty": "medium",
                "language": language,
                "correct_answer": "amebeba",
                "acceptable_answers": ["amebeba"]
            },
            {
                "id": 8,
                "question": "'Ninasoma kitabu' kwa Kiingereza",
                "category": "Translation",
                "difficulty": "medium",
                "language": language,
                "correct_answer": "i am reading a book",
                "acceptable_answers": ["i am reading a book", "i'm reading a book", "am reading a book"]
            },
            {
                "id": 9,
                "question": "-----wa watu (umati/kamati)",
                "category": "Vocabulary",
                "difficulty": "easy",
                "language": language,
                "correct_answer": "umati",
                "acceptable_answers": ["umati"]
            },
            {
                "id": 10,
                "question": "kanusha 'keti'",
                "category": "Vocabulary",
                "difficulty": "easy",
                "language": language,
                "correct_answer": "simama",
                "acceptable_answers": ["simama", "stand"]
            },
        ],
        "Kikuyu": [
            {
                "id": 1,
                "question": "Nĩngwendete nĩ kuaga atĩa na gĩthũngũ?",
                "category": "Translation",
                "difficulty": "easy",
                "language": language,
                "correct_answer": "i love you",
                "acceptable_answers": ["i love you", "love you", "i love u"]
            },
            {
                "id": 2,
                "question": "Maitu ---- thoko ũmũthĩ (niarathire/niathire)",
                "category": "Grammar",
                "difficulty": "medium",
                "language": language,
                "correct_answer": "niathire",
                "acceptable_answers": ["niathire"]
            },
            {
                "id": 3,
                "question": "Kũina nĩ kuga atĩa na gĩthweri",
                "category": "Translation",
                "difficulty": "easy",
                "language": language,
                "correct_answer": "singing",
                "acceptable_answers": ["singing", "to sing", "sing"]
            },
            {
                "id": 4,
                "question": "Ciana irathomothio nĩ ----- (mwarimũ/mũrũtwo)",
                "category": "Grammar",
                "difficulty": "medium",
                "language": language,
                "correct_answer": "mwarimũ",
                "acceptable_answers": ["mwarimũ", "mwarimu"]
            },
            {
                "id": 5,
                "question": "Mwaki nĩ ------- thaa ici (wakanire/wakana)",
                "category": "Grammar",
                "difficulty": "medium",
                "language": language,
                "correct_answer": "wakana",
                "acceptable_answers": ["wakana"]
            },
            {
                "id": 6,
                "question": "Andika namba kenda",
                "category": "Numbers",
                "difficulty": "easy",
                "language": language,
                "correct_answer": "9",
                "acceptable_answers": ["9", "nine", "kenda"]
            },
            {
                "id": 7,
                "question": "Gikombe gĩkĩ ------ (nĩgĩatũka/nakaunĩka)",
                "category": "Grammar",
                "difficulty": "medium",
                "language": language,
                "correct_answer": "nĩgĩatũka",
                "acceptable_answers": ["nĩgĩatũka", "nigiathuka"]
            },
            {
                "id": 8,
                "question": "Rangi mũtune ũhana kĩ--- (thakame/iria)",
                "category": "Vocabulary",
                "difficulty": "easy",
                "language": language,
                "correct_answer": "thakame",
                "acceptable_answers": ["thakame"]
            },
            {
                "id": 9,
                "question": "Ritwa rĩngĩ rĩa mwarimũ nĩ ------ (ndagĩtarĩ/mũrutani)",
                "category": "Vocabulary",
                "difficulty": "easy",
                "language": language,
                "correct_answer": "mũrutani",
                "acceptable_answers": ["mũrutani", "murutani"]
            },
            {
                "id": 10,
                "question": "kiondo ---- nĩ kĩrataruka (icio/gĩkĩ)",
                "category": "Grammar",
                "difficulty": "medium",
                "language": language,
                "correct_answer": "gĩkĩ",
                "acceptable_answers": ["gĩkĩ", "giki"]
            },
        ],
        "English": [
            {"question": "What is the past tense of 'go'?", "category": "grammar", "difficulty": "easy", "language": language, "correct_answer": "went", "acceptable_answers": ["went"]},
            {"question": "Complete: 'She ___ to school every day' (goes/go)", "category": "grammar", "difficulty": "easy", "language": language, "correct_answer": "goes", "acceptable_answers": ["goes"]},
            {"question": "What is the plural of 'child'?", "category": "vocabulary", "difficulty": "easy", "language": language, "correct_answer": "children", "acceptable_answers": ["children"]},
            {"question": "Choose the correct article: '___ apple' (a/an)", "category": "grammar", "difficulty": "easy", "language": language, "correct_answer": "an", "acceptable_answers": ["an"]},
            {"question": "What does 'beautiful' mean?", "category": "vocabulary", "difficulty": "easy", "language": language, "correct_answer": "attractive", "acceptable_answers": ["attractive", "pretty", "good-looking", "lovely"]},
            {"question": "Complete: 'I ___ a student' (am/is/are)", "category": "grammar", "difficulty": "easy", "language": language, "correct_answer": "am", "acceptable_answers": ["am"]},
            {"question": "What is the past tense of 'eat'?", "category": "grammar", "difficulty": "easy", "language": language, "correct_answer": "ate", "acceptable_answers": ["ate"]},
            {"question": "Choose: 'He ___ playing' (is/are)", "category": "grammar", "difficulty": "easy", "language": language, "correct_answer": "is", "acceptable_answers": ["is"]},
            {"question": "What is the plural of 'mouse'?", "category": "vocabulary", "difficulty": "medium", "language": language, "correct_answer": "mice", "acceptable_answers": ["mice"]},
            {"question": "Complete: 'They ___ happy' (is/are)", "category": "grammar", "difficulty": "easy", "language": language, "correct_answer": "are", "acceptable_answers": ["are"]},
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
        
        # Only show speech input for Kiswahili and English (not supported for Kikuyu)
        if selected_lang_info['name'] != "Kikuyu":
            st.session_state.speech_input_enabled = st.checkbox(
                "Enable Speech Input (STT)",
                value=st.session_state.speech_input_enabled,
                help="Enable speech-to-text for questions"
            )
        else:
            # Disable speech input for Kikuyu
            st.session_state.speech_input_enabled = False
            st.caption("ℹ️ Speech input not available for Kikuyu")
        
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
    """Process chat query leveraging GPT-4's strong language capabilities"""
    st.session_state.chat_history.append({"role": "user", "content": query})
    
    with st.spinner("🤔 Thinking..."):
        try:
            # Create prompt template
            prompt_template = create_language_tutor_prompt()
            
            # Retrieve relevant context if vectorstore available
            context = ""
            if vectorstore:
                retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
                docs = retriever.get_relevant_documents(query)
                if docs:
                    context = "\n\n".join([doc.page_content for doc in docs])
            
            # Add Gĩkũyũ dictionary to context if teaching Kikuyu
            if lang_info['name'] == "Kikuyu":
                dictionary_context = "\n\nVERIFIED GĨKŨYŨ VOCABULARY (use ONLY these):\n"
                dictionary_context += "\nNouns:\n"
                for word, meaning in GIKUYU_DICTIONARY["nouns"].items():
                    dictionary_context += f"- {word}: {meaning}\n"
                dictionary_context += "\nVerbs:\n"
                for word, meaning in GIKUYU_DICTIONARY["verbs"].items():
                    dictionary_context += f"- {word}: {meaning}\n"
                dictionary_context += "\nGreetings/Phrases:\n"
                for word, meaning in GIKUYU_DICTIONARY["greetings_phrases"].items():
                    dictionary_context += f"- {word}: {meaning}\n"
                dictionary_context += "\nNumbers:\n"
                for word, meaning in GIKUYU_DICTIONARY["numbers"].items():
                    dictionary_context += f"- {word}: {meaning}\n"
                
                context = dictionary_context + "\n\n" + context
            
            # Provide context
            if context:
                context_instruction = f"Relevant knowledge base information:\n\n{context}\n\nUse this as reference along with your GPT-4 knowledge to provide accurate, helpful answers."
            else:
                context_instruction = f"Use your GPT-4 knowledge of {lang_info['name']} to provide accurate, helpful guidance."
            
            # Format prompt with context
            formatted_prompt = prompt_template.format_messages(
                language=lang_info['name'],
                context=context_instruction,
                input=query
            )
            
            # Generate response
            response = llm.invoke(formatted_prompt)
            answer = response.content
            
            # Validate and correct Gĩkũyũ responses for hallucinations
            corrected_answer, had_errors, corrections = validate_gikuyu_response(answer, lang_info)
            
            # If hallucinations were detected, show warning
            if had_errors:
                st.warning("⚠️ Hallucination detected and corrected!")
                
                # Show what was corrected
                with st.expander("🔍 See what was corrected"):
                    st.markdown("**Swahili/Sheng words incorrectly used:**")
                    for correction in corrections:
                        st.markdown(f"""
                        <div class='correction-box'>
                            <p>❌ <strong>Error:</strong> {correction['error']}</p>
                            <p>✅ <strong>Correct Gĩkũyũ:</strong> {correction['correct']}</p>
                            <p>💡 <strong>Note:</strong> {correction['note']}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                # Use corrected answer
                answer = corrected_answer
            
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
        
        if st.button("🎲 Start Quiz (5 Questions)", use_container_width=True):
            with st.spinner(f"🤖 Generating {lang_info['name']} quiz questions..."):
                st.session_state.quiz_questions = generate_quiz_questions(lang_info['name'], num_questions=5)
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
        
        # Check if this question has been answered
        question_answered = len(st.session_state.quiz_answers) > st.session_state.current_quiz_index
        
        if not question_answered:
            # Show answer input and submit button
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
                        # Simple string matching - NO AI evaluation
                        user_lower = user_answer.lower().strip()
                        
                        # Get acceptable answers
                        acceptable_answers = current_q.get('acceptable_answers', [current_q.get('correct_answer', '')])
                        
                        # Check if answer matches any acceptable answer
                        is_correct = any(user_lower == ans.lower().strip() for ans in acceptable_answers)
                        
                        # Language-specific feedback
                        if lang_info['name'] == "Kiswahili":
                            correct_msg = "Sahihi! Umefanya vizuri!"
                            incorrect_msg = "Si sahihi. Jaribu tena!"
                        elif lang_info['name'] == "Kikuyu":
                            correct_msg = "Nĩ wega! Wĩkĩte wega mũno!"
                            incorrect_msg = "Ti wega. Geria rĩngĩ!"
                        else:
                            correct_msg = "Correct! Excellent work!"
                            incorrect_msg = "Not quite right. Try again!"
                        
                        # Store answer
                        st.session_state.quiz_answers.append({
                            "question": current_q['question'],
                            "user_answer": user_answer,
                            "correct": is_correct,
                            "explanation": current_q.get('explanation', ''),
                            "correct_answer": current_q.get('correct_answer', ''),
                            "teaching_point": ""
                        })
                        
                        if is_correct:
                            st.session_state.quiz_score += 1
                        
                        st.rerun()
                    else:
                        st.warning("Please enter an answer before submitting!")
            
            with col2:
                if st.button("⏭️ Skip Question", use_container_width=True):
                    st.session_state.quiz_answers.append({
                        "question": current_q['question'],
                        "user_answer": "Skipped",
                        "correct": False,
                        "explanation": "You skipped this question.",
                        "correct_answer": current_q.get('correct_answer', ''),
                        "teaching_point": ""
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
            # Question has been answered - show feedback and Next button
            answer_data = st.session_state.quiz_answers[st.session_state.current_quiz_index]
            
            if answer_data['correct']:
                # Show success message
                st.success("✅ Well done!")
            else:
                # Show error with correct answer
                st.error("❌ Not correct.")
                st.info(f"**Correct answer:** {answer_data['correct_answer']}")
            
            # Show English reference for context (Kikuyu only)
            if current_q.get('english_reference') and lang_info['name'] == "Kikuyu":
                st.caption(f"📖 English: {current_q['english_reference']}")
            
            st.markdown("---")
            
            # Language-specific button text
            if lang_info['name'] == "Kiswahili":
                next_text = "➡️ Swali Linalofuata"
            elif lang_info['name'] == "Kikuyu":
                next_text = "➡️ Kĩũria Kĩrĩa Kĩngĩ"
            else:
                next_text = "➡️ Next Question"
            
            # Prominent Next button OUTSIDE all nested blocks
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button(next_text, type="primary", use_container_width=True, key=f"next_btn_{st.session_state.current_quiz_index}"):
                    st.session_state.current_quiz_index += 1
                    st.rerun()
    
    else:
        # Quiz completed - show results
        total_questions = len(st.session_state.quiz_questions)
        score = st.session_state.quiz_score
        percentage = (score / total_questions) * 100
        
        # Determine pass/fail
        passed = percentage >= 60  # 60% passing grade
        
        # Determine colors and messages
        bg_color = "#4CAF50" if passed else "#f44336"
        accent_color = "#8BC34A" if passed else "#e57373"
        title = "🎉 Congratulations! You Passed!" if passed else "📚 Keep Practicing!"
        
        if percentage >= 80:
            message = "Excellent work! You have a strong understanding."
        elif passed:
            message = "Good job! You passed the quiz."
        else:
            message = "Do not worry! Review the material and try again."
        
        # Display results without complex f-string
        percentage_display = f"{percentage:.1f}%"
        result_html = f"""
        <div style="background: linear-gradient(135deg, {bg_color} 0%, {accent_color} 100%); padding: 2rem; border-radius: 1rem; color: white; text-align: center; margin: 2rem 0;">
            <h2>{title}</h2>
            <h1 style="font-size: 3rem; margin: 1rem 0;">{score}/{total_questions}</h1>
            <h3>{percentage_display}</h3>
            <p style="font-size: 1.2rem; margin-top: 1rem;">{message}</p>
        </div>
        """
        st.markdown(result_html, unsafe_allow_html=True)
        
        # Show detailed results
        st.markdown("### 📊 Detailed Review")
        
        for i, answer in enumerate(st.session_state.quiz_answers, 1):
            status = "✅" if answer['correct'] else "❌"
            st.markdown(f"""
            <div class='{"feature-box" if answer["correct"] else "correction-box"}'>
                <h4>{status} Question {i}: {answer['question']}</h4>
                <p><strong>Your Answer:</strong> {answer['user_answer']}</p>
                {f"<p><strong>Correct Answer:</strong> {answer.get('correct_answer', '')}</p>" if not answer['correct'] and answer.get('correct_answer') else ""}
            </div>
            """, unsafe_allow_html=True)
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        # Check if this was the first 5 questions (for Kikuyu and Kiswahili)
        if total_questions == 5 and lang_info['name'] in ["Kikuyu", "Kiswahili"]:
            with col1:
                if st.button("➕ Continue with 5 More Questions", use_container_width=True):
                    # Load questions 6-10
                    all_questions = generate_fallback_questions(lang_info['name'])
                    st.session_state.quiz_questions = all_questions[5:10]
                    st.session_state.current_quiz_index = 0
                    # Keep the score from first 5
                    st.session_state.quiz_answers = []
                    st.rerun()
            
            with col2:
                if st.button("🔄 Restart Quiz", use_container_width=True):
                    st.session_state.quiz_questions = []
                    st.session_state.current_quiz_index = 0
                    st.session_state.quiz_score = 0
                    st.session_state.quiz_answers = []
                    st.rerun()
            
            with col3:
                if st.button("📚 Back to Learning", use_container_width=True):
                    st.session_state.current_mode = "chat"
                    st.rerun()
        else:
            with col1:
                if st.button("🔄 Take New Quiz", use_container_width=True):
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
                
                # Create AI prompt for vocabulary search with anti-hallucination instructions
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
                
                # Validate for hallucinations if Gĩkũyũ
                corrected_answer, had_errors, corrections = validate_gikuyu_response(answer, lang_info)
                
                # Display AI response
                st.success(f"✅ Found information for: '{search_term}'")
                
                # Show hallucination warning if detected
                if had_errors:
                    st.warning("⚠️ Hallucination detected and corrected!")
                    with st.expander("🔍 See what was corrected"):
                        for correction in corrections:
                            st.markdown(f"""
                            <div class='correction-box'>
                                <p>❌ <strong>Error:</strong> {correction['error']}</p>
                                <p>✅ <strong>Correct:</strong> {correction['correct']}</p>
                                <p>💡 {correction['note']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                    answer = corrected_answer
                
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
        st.info(f"""Try asking:
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
    
    # Different categories based on language
    if lang_info['name'] == "Kikuyu":
        categories = {
            "Family": "family members like mother, father, sister, brother",
            "Food": "common foods and meals",
            "Animals": "common animals",
            "Numbers": "numbers 1-20"
        }
    else:
        # Same categories for Kiswahili and English
        categories = {
            "Family": "family members like mother, father, sister, brother",
            "Food": "common foods and meals",
            "Numbers": "numbers 1-20",
            "Animals": "common animals"
        }
    
    cols = st.columns(4)
    
    # Initialize session state for selected category
    if 'selected_vocab_category' not in st.session_state:
        st.session_state.selected_vocab_category = None
    
    for i, (category, description) in enumerate(categories.items()):
        col = cols[i % 4]
        with col:
            if st.button(f"📂 {category}", use_container_width=True, key=f"cat_{category}"):
                st.session_state.selected_vocab_category = (category, description)
                st.rerun()
    
    # Display selected category content
    if st.session_state.selected_vocab_category:
        category, description = st.session_state.selected_vocab_category
        
        # Clear button
        if st.button("🔙 Back to Categories", key="back_to_categories"):
            st.session_state.selected_vocab_category = None
            st.rerun()
        
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
                category_answer = response.content
                
                # Validate for hallucinations if Gĩkũyũ
                corrected_answer, had_errors, corrections = validate_gikuyu_response(category_answer, lang_info)
                
                if had_errors:
                    st.warning("⚠️ Hallucinations corrected in this list")
                    category_answer = corrected_answer
                
                st.markdown(f"""
                <div class='feature-box'>
                    <h4>📂 {category} Vocabulary</h4>
                    {category_answer.replace(chr(10), '<br>')}
                </div>
                """, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error loading category: {str(e)}")

if __name__ == "__main__":
    main()