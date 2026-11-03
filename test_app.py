#!/usr/bin/env python3
"""
Quick test script to verify the application components work correctly
"""

import os
import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import torch
        print("  + PyTorch")
    except ImportError:
        print("  - PyTorch - Run: pip install torch")
        return False
    
    try:
        import torchvision
        print("  + TorchVision")
    except ImportError:
        print("  - TorchVision - Run: pip install torchvision")
        return False
    
    try:
        from efficientnet_pytorch import EfficientNet
        print("  + EfficientNet")
    except ImportError:
        print("  - EfficientNet - Run: pip install efficientnet-pytorch")
        return False
    
    try:
        import flask
        print("  + Flask")
    except ImportError:
        print("  - Flask - Run: pip install flask")
        return False
    
    try:
        import openai
        print("  + OpenAI")
    except ImportError:
        print("  - OpenAI - Run: pip install openai")
        return False
    
    return True

def test_project_structure():
    """Test if project structure is correct"""
    print("\nTesting project structure...")
    
    required_files = [
        'app.py',
        'predictor.py', 
        'model_trainer.py',
        'data_preprocessor.py',
        'medical_report_generator.py',
        'requirements.txt',
        '.env'
    ]
    
    required_dirs = [
        'templates',
        'static',
        'static/css',
        'static/js',
        'static/images',
        'models',
        'uploads'
    ]
    
    all_good = True
    
    for file in required_files:
        if os.path.exists(file):
            print(f"  + {file}")
        else:
            print(f"  - {file}")
            all_good = False
    
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"  + {directory}/")
        else:
            print(f"  - {directory}/")
            all_good = False
    
    return all_good

def test_dataset():
    """Test if dataset is available"""
    print("\nTesting dataset...")
    
    dataset_dir = 'DATASET'
    if not os.path.exists(dataset_dir):
        print(f"  - {dataset_dir} directory not found")
        return False
    
    required_subdirs = ['train', 'valid', 'test']
    for subdir in required_subdirs:
        path = os.path.join(dataset_dir, subdir)
        if os.path.exists(path):
            print(f"  + {path}")
        else:
            print(f"  - {path}")
            return False
    
    return True

def test_model_components():
    """Test if model components can be initialized"""
    print("\nTesting model components...")
    
    try:
        from data_preprocessor import ImagePreprocessor
        preprocessor = ImagePreprocessor()
        print("  + ImagePreprocessor")
    except Exception as e:
        print(f"  - ImagePreprocessor: {e}")
        return False
    
    try:
        from medical_report_generator import MedicalReportGenerator
        report_gen = MedicalReportGenerator()
        print("  + MedicalReportGenerator")
    except Exception as e:
        print(f"  - MedicalReportGenerator: {e}")
        return False
    
    try:
        from predictor import LungCancerPredictor
        # This will work even without a trained model
        predictor = LungCancerPredictor()
        print("  + LungCancerPredictor")
    except Exception as e:
        print(f"  - LungCancerPredictor: {e}")
        return False
    
    return True

def main():
    print("Lung Cancer Classifier - System Test")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports),
        ("Project Structure", test_project_structure), 
        ("Dataset Check", test_dataset),
        ("Model Components", test_model_components)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 40)
    print("TEST RESULTS:")
    
    all_passed = True
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  {test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("+ All tests passed! The application should work correctly.")
        print("\nTo start the application, run:")
        print("  python app.py")
        print("  or")
        print("  python run.py")
    else:
        print("- Some tests failed. Please fix the issues above.")
        print("\nCommon solutions:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Run setup script: python setup.py")
        print("  3. Check dataset location and structure")

if __name__ == "__main__":
    main()