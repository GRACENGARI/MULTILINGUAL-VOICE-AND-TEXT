import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
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
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

if not google_api_key:
    raise ValueError("GOOGLE_API_KEY is not set. Check your .env file.")

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
    "Luo": {
        "code": "luo",
        "name": "Luo",
        "greeting": "Oyawore! Rwaki e puonj Luo.",
        "description": "Learn Luo grammar, vocabulary, and sentence construction",
        "tts_lang": "en"  # Fallback to English
    },
    "Kalenjin": {
        "code": "kal",
        "name": "Kalenjin",
        "greeting": "Chamge! Boisho ak kole Kalenjin.",
        "description": "Learn Kalenjin grammar, vocabulary, and sentence construction",
        "tts_lang": "en"  # Fallback to English
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

def get_speech_input():
    """Get speech input from user (placeholder for future implementation)"""
    st.info("🎤 Speech input feature coming soon! For now, please type your question.")
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
if 'voice_enabled' not in st.session_state:
    st.session_state.voice_enabled = False
if 'auto_play_responses' not in st.session_state:
    st.session_state.auto_play_responses = False

def load_language_knowledge_from_json(language):
    """Load language knowledge from JSON files"""
    try:
        filename_map = {
            "Kiswahili": "kiswahili_knowledge.json",
            "Kikuyu": "kikuyu_knowledge.json", 
            "Luo": "luo_knowledge.json",
            "Kalenjin": "kalenjin_knowledge.json"
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
    """Initialize the language model"""
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",  # Using the latest stable Gemini 2.5 Flash
        temperature=0.3,
        max_tokens=None,
        timeout=None
    )

def create_language_tutor_prompt():
    """Create specialized prompt for language tutoring"""
    system_prompt = """You are an expert AI tutor for African languages, specializing in {language}. 
    Your role is to help learners improve their grammar, vocabulary, and sentence construction.

    Guidelines:
    1. Provide clear, simple explanations suitable for all learning levels
    2. Give examples in both the target language and English
    3. Correct mistakes gently and explain why corrections are needed
    4. Support code-switching (mixing languages) as it's natural in African contexts
    5. Encourage use of the local language while being patient with learners
    6. Provide cultural context when relevant
    7. Generate practice exercises and quizzes when requested

    When analyzing input:
    - For vocabulary: provide meaning, part of speech, usage examples
    - For grammar: explain structure, rules, and common patterns
    - For sentences: check grammar, suggest improvements, offer alternatives
    - For errors: explain mistakes clearly and provide correct versions

    Always be encouraging and culturally sensitive.
    
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
        
        # Create embeddings and vector store with latest embedding model
        embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        vectorstore = FAISS.from_documents(splits, embeddings)
        
        return vectorstore
    except Exception as e:
        st.warning(f"Knowledge base setup issue: {str(e)}. Using direct LLM mode.")
        return None

def generate_quiz_questions(language, topic="general"):
    """Generate quiz questions for the selected language"""
    quiz_prompts = {
        "vocabulary": [
            f"What does 'mtu' mean in {language}?",
            f"Translate 'house' to {language}",
            f"What is the plural of 'kitabu' in {language}?"
        ],
        "grammar": [
            f"Complete the sentence in {language}: 'Mimi _____ kitabu' (I am reading a book)",
            f"What is the correct noun class agreement for 'kitabu kizuri' in {language}?",
            f"Form the past tense of 'kusoma' (to read) in {language}"
        ]
    }
    
    questions = []
    for category, q_list in quiz_prompts.items():
        for q in q_list:
            questions.append({
                "question": q,
                "category": category,
                "language": language
            })
    
    return random.sample(questions, min(5, len(questions)))

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
            "Enable Voice Features",
            value=st.session_state.voice_enabled,
            help="Enable text-to-speech for responses"
        )
        
        if st.session_state.voice_enabled:
            st.session_state.auto_play_responses = st.checkbox(
                "Auto-play Responses",
                value=st.session_state.auto_play_responses,
                help="Automatically play audio for AI responses"
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
    
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "Type your question here:",
            placeholder=f"e.g., 'How do I say hello in {lang_info['name']}?' or 'Check this sentence: Mimi ninasoma'",
            label_visibility="collapsed"
        )
        
        col1, col2, col3 = st.columns([2, 1, 2])
        with col2:
            submit = st.form_submit_button("Send 📤", use_container_width=True)
        
        # Voice input option (placeholder)
        if st.session_state.voice_enabled:
            st.caption("🎤 Voice input coming soon - for now, please type your question")
        
        if submit and user_input:
            handle_chat_query(user_input, vectorstore, llm, lang_info)

def handle_chat_query(query, vectorstore, llm, lang_info):
    """Process chat query and generate response"""
    st.session_state.chat_history.append({"role": "user", "content": query})
    
    with st.spinner("🤔 Thinking..."):
        try:
            # Create prompt template
            prompt_template = create_language_tutor_prompt()
            
            if vectorstore:
                # Use RAG if knowledge base available
                retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
                question_answer_chain = create_stuff_documents_chain(llm, prompt_template)
                rag_chain = create_retrieval_chain(retriever, question_answer_chain)
                
                response = rag_chain.invoke({
                    "input": query,
                    "language": lang_info['name']
                })
                answer = response["answer"]
            else:
                # Direct LLM query
                formatted_prompt = prompt_template.format_messages(
                    language=lang_info['name'],
                    context="",
                    input=query
                )
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
    """Display quiz practice interface"""
    st.markdown(f"### 🎯 {lang_info['name']} Quiz Practice")
    
    if not st.session_state.quiz_questions:
        if st.button("🎲 Generate New Quiz"):
            st.session_state.quiz_questions = generate_quiz_questions(lang_info['name'])
            st.session_state.current_quiz_index = 0
            st.rerun()
        
        st.info("Click 'Generate New Quiz' to start practicing!")
        return
    
    # Display current question
    if st.session_state.current_quiz_index < len(st.session_state.quiz_questions):
        current_q = st.session_state.quiz_questions[st.session_state.current_quiz_index]
        
        st.markdown(f"""
        <div class='quiz-question'>
            <h4>Question {st.session_state.current_quiz_index + 1} of {len(st.session_state.quiz_questions)}</h4>
            <p><strong>{current_q['question']}</strong></p>
            <small>Category: {current_q['category'].title()}</small>
        </div>
        """, unsafe_allow_html=True)
        
        # Answer input
        user_answer = st.text_input("Your answer:", key=f"quiz_answer_{st.session_state.current_quiz_index}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("✅ Submit Answer"):
                if user_answer:
                    # Here you would typically check the answer
                    st.success("Answer submitted! (In a full implementation, this would be evaluated)")
                    st.session_state.current_quiz_index += 1
                    st.rerun()
        
        with col2:
            if st.button("⏭️ Skip Question"):
                st.session_state.current_quiz_index += 1
                st.rerun()
        
        with col3:
            if st.button("🔄 New Quiz"):
                st.session_state.quiz_questions = []
                st.session_state.current_quiz_index = 0
                st.rerun()
    
    else:
        st.success("🎉 Quiz completed!")
        if st.button("🔄 Start New Quiz"):
            st.session_state.quiz_questions = []
            st.session_state.current_quiz_index = 0
            st.rerun()

def show_vocabulary_interface(lang_info):
    """Display vocabulary building interface"""
    st.markdown(f"### 📖 {lang_info['name']} Vocabulary Builder")
    
    # Search vocabulary
    search_term = st.text_input("🔍 Search for a word:", placeholder="Enter a word in English or " + lang_info['name'])
    
    if search_term:
        # In a full implementation, this would search the vocabulary database
        st.markdown(f"""
        <div class='feature-box'>
            <h4>Search Results for: "{search_term}"</h4>
            <p><em>In a full implementation, this would show vocabulary entries, definitions, examples, and audio pronunciation.</em></p>
        </div>
        """, unsafe_allow_html=True)
    
    # Common vocabulary categories
    st.markdown("### 📚 Browse by Category")
    
    categories = ["Family", "Food", "Colors", "Numbers", "Greetings", "Time", "Animals", "Body Parts"]
    
    cols = st.columns(4)
    for i, category in enumerate(categories):
        col = cols[i % 4]
        with col:
            if st.button(f"📂 {category}", use_container_width=True):
                st.info(f"Loading {category} vocabulary... (Feature in development)")

if __name__ == "__main__":
    main()