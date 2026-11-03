#!/usr/bin/env python3
"""
Simple launcher script for the Lung Cancer Classifier web application
"""

import os
import sys
import subprocess

def main():
    print("Lung Cancer Classifier - Web Application")
    print("=" * 45)
    
    # Check if required files exist
    required_files = ['app.py', 'requirements.txt', '.env']
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"Missing required files: {', '.join(missing_files)}")
        print("Please run setup.py first or ensure all files are present.")
        return
    
    # Check if uploads directory exists
    if not os.path.exists('uploads'):
        os.makedirs('uploads', exist_ok=True)
        print("Created uploads directory")
    
    # Check if static/images directory exists
    if not os.path.exists('static/images'):
        os.makedirs('static/images', exist_ok=True)
        print("Created static/images directory")
    
    print("\nStarting the web application...")
    print("Open your browser and go to: http://localhost:5000")
    print("Login with any username/password combination")
    print("\nPress Ctrl+C to stop the server")
    print("-" * 45)
    
    try:
        # Run the Flask application
        subprocess.run([sys.executable, 'app.py'], check=True)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\nError running application: {e}")
        print("Please check the error messages above and ensure all dependencies are installed.")

if __name__ == "__main__":
    main()