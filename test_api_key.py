#!/usr/bin/env python3
"""
Test script to check Google API key and available models
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

print("=" * 60)
print("🔑 Testing Google API Key")
print("=" * 60)

if not api_key:
    print("❌ No API key found in .env file")
    exit(1)

print(f"✅ API Key found: {api_key[:20]}...")

# Configure the API
genai.configure(api_key=api_key)

print("\n📋 Listing available models...")
print("-" * 60)

try:
    models = genai.list_models()
    
    print("\n✅ Available models:")
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"  ✓ {model.name}")
            print(f"    Description: {model.description[:80]}...")
            print()
    
    print("\n🎯 Recommended models for this project:")
    print("  - gemini-pro (Standard model)")
    print("  - gemini-1.5-flash (Fast model)")
    print("  - gemini-1.5-pro (Advanced model)")
    
except Exception as e:
    print(f"\n❌ Error listing models: {str(e)}")
    print("\n💡 Possible solutions:")
    print("1. Check if your API key is valid")
    print("2. Enable 'Generative Language API' at:")
    print("   https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com")
    print("3. Create a new API key at:")
    print("   https://makersuite.google.com/app/apikey")

print("\n" + "=" * 60)
print("🧪 Testing a simple generation...")
print("=" * 60)

try:
    # Try to use the model
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Say hello in Kiswahili")
    print(f"\n✅ Success! Response: {response.text}")
    print("\n🎉 Your API key is working correctly!")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    print("\n💡 Your API key might not have access to Gemini models.")
    print("   Please visit: https://makersuite.google.com/app/apikey")
    print("   And create a new API key with Gemini access.")

print("\n" + "=" * 60)