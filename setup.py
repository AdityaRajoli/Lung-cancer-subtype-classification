#!/usr/bin/env python3
"""
Setup script for the Lung Cancer Classifier project
Handles initial setup, dependency installation, and basic configuration
"""

import os
import sys
import subprocess
import platform

def print_header():
    print("🫁 Lung Cancer Classifier - Setup Script")
    print("=" * 50)
    print("Setting up your clinical-grade AI diagnostic system...")
    print()

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required!")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def create_directories():
    """Create necessary directories"""
    directories = [
        'models',
        'uploads', 
        'static/images',
        'static/css',
        'static/js'
    ]
    
    print("📁 Creating project directories...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   ✅ {directory}")

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies!")
        print("Please run: pip install -r requirements.txt")
        return False

def setup_environment():
    """Setup environment file if it doesn't exist"""
    env_file = '.env'
    if not os.path.exists(env_file):
        print(f"\n🔧 Creating {env_file} file...")
        with open(env_file, 'w') as f:
            f.write("# Lung Cancer Classifier Environment Variables\n")
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
            f.write("FLASK_SECRET_KEY=your_secret_key_here\n")
        print(f"✅ {env_file} created!")
        print("⚠️  Please update the API keys in the .env file")
    else:
        print(f"✅ {env_file} already exists")

def create_sample_assets():
    """Create sample confusion matrix"""
    print("\n🎨 Creating sample assets...")
    try:
        subprocess.check_call([sys.executable, 'create_sample_confusion_matrix.py'])
        print("✅ Sample confusion matrix created!")
    except subprocess.CalledProcessError:
        print("⚠️  Could not create sample confusion matrix")
        print("You can run: python create_sample_confusion_matrix.py")

def check_dataset():
    """Check if dataset exists"""
    dataset_dir = 'DATASET'
    if os.path.exists(dataset_dir):
        print(f"✅ Dataset directory found: {dataset_dir}")
        
        # Check for required subdirectories
        required_dirs = ['train', 'valid', 'test']
        for subdir in required_dirs:
            path = os.path.join(dataset_dir, subdir)
            if os.path.exists(path):
                print(f"   ✅ {subdir} directory found")
            else:
                print(f"   ⚠️  {subdir} directory missing")
    else:
        print(f"⚠️  Dataset directory not found: {dataset_dir}")
        print("Please ensure the DATASET folder is in the project root")

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎉 Setup completed!")
    print("\n📋 Next Steps:")
    print("1. Update API keys in .env file:")
    print("   - Get OpenAI API key from: https://platform.openai.com/api-keys")
    print("   - Set FLASK_SECRET_KEY to a random string")
    print()
    print("2. Optional - Train the model:")
    print("   python train_model.py")
    print()
    print("3. Run the application:")
    print("   python app.py")
    print()
    print("4. Open your browser and go to:")
    print("   http://localhost:5000")
    print()
    print("🔐 Login with any username/password combination")
    print()
    print("📚 For more information, see README.md")

def main():
    """Main setup function"""
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        print("\n⚠️  Setup completed with warnings.")
        print("Please install dependencies manually and run setup again.")
        return
    
    # Setup environment
    setup_environment()
    
    # Create sample assets
    create_sample_assets()
    
    # Check dataset
    check_dataset()
    
    # Print next steps
    print_next_steps()

if __name__ == "__main__":
    main()