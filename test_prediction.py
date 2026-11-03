#!/usr/bin/env python3
"""
Test the improved prediction system
"""

from predictor import LungCancerPredictor
import os

def test_predictions():
    print("Testing Enhanced Prediction System")
    print("=" * 40)
    
    predictor = LungCancerPredictor()
    
    # Test with sample images from dataset
    test_cases = [
        ("DATASET/test/adenocarcinoma/000108 (3).png", "Adenocarcinoma"),
        ("DATASET/test/large.cell.carcinoma/000108.png", "Large Cell Carcinoma"),
        ("DATASET/test/normal/10.png", "Normal"),
        ("DATASET/test/squamous.cell.carcinoma/000108 (6).png", "Squamous Cell Carcinoma")
    ]
    
    for image_path, expected in test_cases:
        if os.path.exists(image_path):
            print(f"\nTesting: {os.path.basename(image_path)}")
            print(f"Expected: {expected}")
            
            result = predictor.predict(image_path)
            
            print(f"Predicted: {result['predicted_class']}")
            print(f"Confidence: {result['confidence']:.1%}")
            
            print("Class Probabilities:")
            for class_name, prob in result['class_probabilities'].items():
                print(f"  {class_name}: {prob:.1%}")
            
            # Check if prediction is correct
            correct = expected.lower() in result['predicted_class'].lower()
            print(f"Result: {'CORRECT' if correct else 'INCORRECT'}")
            print("-" * 40)
        else:
            print(f"Image not found: {image_path}")

if __name__ == "__main__":
    test_predictions()