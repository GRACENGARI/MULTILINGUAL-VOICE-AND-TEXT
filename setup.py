#!/usr/bin/env python3
"""
Setup script for African Language Tutor
Helps users set up the environment and dependencies
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write("# African Language Tutor Environment Variables\n")
            f.write("# Get your API key from: https://makersuite.google.com/app/apikey\n")
            f.write("GOOGLE_API_KEY='your_google_api_key_here'\n")
        print("✅ Created .env file - please add your Google API key")
        return False
    else:
        print("✅ .env file already exists")
        return True

def install_dependencies():
    """Install required dependencies"""
    try:
        print("📦 Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def check_api_key():
    """Check if API key is configured"""
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key and api_key != "your_google_api_key_here" and api_key.strip():
            print("✅ Google API key is configured")
            return True
        else:
            print("⚠️  Google API key not configured in .env file")
            return False
    except ImportError:
        print("⚠️  Cannot check API key - dotenv not installed yet")
        return False

def create_directories():
    """Create necessary directories"""
    directories = ["language_data"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"✅ Directory exists: {directory}")

def run_demo():
    """Run the demo script"""
    try:
        print("\n🚀 Running demo...")
        subprocess.check_call([sys.executable, "demo_script.py"])
        return True
    except subprocess.CalledProcessError:
        print("❌ Demo failed to run")
        return False
    except FileNotFoundError:
        print("⚠️  Demo script not found")
        return False

def main():
    """Main setup function"""
    print("🌍 African Language AI Tutor - Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Create .env file
    env_exists = create_env_file()
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Check API key
    api_configured = check_api_key()
    
    print("\n" + "=" * 50)
    print("📋 Setup Summary:")
    print("=" * 50)
    
    if env_exists and api_configured:
        print("✅ Environment fully configured")
        print("\n🚀 You can now run the application:")
        print("   streamlit run african_language_tutor.py")
        
        # Ask if user wants to run demo
        try:
            response = input("\n🎯 Would you like to run the demo? (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                run_demo()
        except KeyboardInterrupt:
            print("\n👋 Setup completed!")
    else:
        print("⚠️  Setup incomplete:")
        if not env_exists:
            print("   - .env file needs to be created")
        if not api_configured:
            print("   - Google API key needs to be configured in .env file")
        
        print("\n📝 Next steps:")
        print("1. Get a Google AI API key from: https://makersuite.google.com/app/apikey")
        print("2. Add your API key to the .env file")
        print("3. Run: streamlit run african_language_tutor.py")
    
    print("\n📚 For more information, see README.md")

if __name__ == "__main__":
    main()