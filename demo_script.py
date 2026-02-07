#!/usr/bin/env python3
"""
Demo script for African Language Tutor
This script demonstrates key features without requiring the full Streamlit interface
"""

import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def load_language_data(language):
    """Load language knowledge from JSON files"""
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
    return None

def demo_vocabulary_lookup(language, word):
    """Demo vocabulary lookup functionality"""
    data = load_language_data(language)
    if not data:
        return f"Language data not found for {language}"
    
    vocab = data.get('vocabulary', {})
    basic_words = vocab.get('basic_words', {})
    greetings = vocab.get('greetings', {})
    
    # Check basic words
    if word in basic_words:
        info = basic_words[word]
        result = f"Word: {word}\n"
        result += f"Meaning: {info.get('meaning', 'N/A')}\n"
        result += f"Part of Speech: {info.get('pos', 'N/A')}\n"
        if 'examples' in info:
            result += "Examples:\n"
            for example in info['examples']:
                result += f"  - {example}\n"
        return result
    
    # Check greetings
    if word in greetings:
        info = greetings[word]
        result = f"Greeting: {word}\n"
        result += f"Meaning: {info.get('meaning', 'N/A')}\n"
        result += f"Response: {info.get('response', 'N/A')}\n"
        result += f"Usage: {info.get('usage', 'N/A')}\n"
        return result
    
    return f"Word '{word}' not found in {language} vocabulary database"

def demo_grammar_rules(language):
    """Demo grammar rules display"""
    data = load_language_data(language)
    if not data:
        return f"Language data not found for {language}"
    
    rules = data.get('grammar_rules', [])
    result = f"Grammar Rules for {language}:\n\n"
    
    for i, rule in enumerate(rules, 1):
        result += f"{i}. {rule.get('rule', 'Unknown Rule')}\n"
        result += f"   Description: {rule.get('description', 'No description')}\n"
        examples = rule.get('examples', [])
        if examples:
            result += "   Examples:\n"
            for example in examples:
                result += f"     - {example}\n"
        result += "\n"
    
    return result

def demo_common_errors(language):
    """Demo common errors and corrections"""
    data = load_language_data(language)
    if not data:
        return f"Language data not found for {language}"
    
    errors = data.get('common_errors', [])
    result = f"Common Errors in {language}:\n\n"
    
    for i, error in enumerate(errors, 1):
        result += f"{i}. Error: {error.get('error', 'Unknown error')}\n"
        result += f"   Correction: {error.get('correct', 'No correction provided')}\n"
        result += f"   Example: {error.get('example', 'No example provided')}\n\n"
    
    return result

def main():
    """Main demo function"""
    print("🌍 African Language AI Tutor - Demo")
    print("=" * 50)
    
    # Test each language
    languages = ["Kiswahili", "Kikuyu", "Luo", "Kalenjin"]
    
    for language in languages:
        print(f"\n📚 Testing {language}:")
        print("-" * 30)
        
        # Test vocabulary lookup
        if language == "Kiswahili":
            test_word = "mtu"
        elif language == "Kikuyu":
            test_word = "mũndũ"
        elif language == "Luo":
            test_word = "dhano"
        else:  # Kalenjin
            test_word = "chito"
        
        print(f"🔍 Vocabulary lookup for '{test_word}':")
        print(demo_vocabulary_lookup(language, test_word))
        
        # Test grammar rules (first rule only for brevity)
        print(f"📝 Grammar rules:")
        grammar_info = demo_grammar_rules(language)
        # Show only first rule to keep output manageable
        lines = grammar_info.split('\n')
        for line in lines[:6]:  # First rule + header
            print(line)
        print("   ... (more rules available)\n")
    
    print("\n✅ Demo completed!")
    print("\nTo run the full application:")
    print("1. Set up your GOOGLE_API_KEY in .env file")
    print("2. Run: streamlit run african_language_tutor.py")

if __name__ == "__main__":
    main()