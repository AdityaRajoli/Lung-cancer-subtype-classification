#!/usr/bin/env python3
"""
Training script for the Lung Cancer Classifier
Run this script to train the EfficientNet-B4 model on the dataset
"""

import os
import sys
from model_trainer import EnhancedTrainer
import torch

def main():
    print("Lung Cancer Classifier - Model Training")
    print("=" * 50)
    
    # Check if CUDA is available
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")
    
    # Initialize trainer
    trainer = EnhancedTrainer(num_classes=4, model_name='efficientnet-b4')
    
    # Dataset path
    data_dir = 'DATASET'
    
    if not os.path.exists(data_dir):
        print(f"Dataset directory '{data_dir}' not found!")
        print("Please ensure the DATASET folder is in the project root.")
        return
    
    # Check dataset structure
    required_dirs = ['train', 'valid', 'test']
    for dir_name in required_dirs:
        dir_path = os.path.join(data_dir, dir_name)
        if not os.path.exists(dir_path):
            print(f"Required directory '{dir_path}' not found!")
            return
    
    print("Dataset structure verified")
    
    # Create models directory
    os.makedirs('models', exist_ok=True)
    
    try:
        print("\nStarting model training...")
        print("This may take 1-3 hours depending on your hardware.")
        
        # Train the model
        model = trainer.train_model(
            data_dir=data_dir,
            epochs=5,
            save_path='models/web_model_b4.pth'
        )
        
        print("\nTraining completed successfully!")
        
        # Evaluate the model
        print("\nEvaluating model performance...")
        report, cm = trainer.evaluate_model('models/web_model_b4.pth', data_dir)
        
        print("\nModel Performance:")
        print(f"Accuracy: {report['accuracy']:.3f}")
        print(f"Macro Avg Precision: {report['macro avg']['precision']:.3f}")
        print(f"Macro Avg Recall: {report['macro avg']['recall']:.3f}")
        print(f"Macro Avg F1-Score: {report['macro avg']['f1-score']:.3f}")
        
        print("\nModel training and evaluation completed!")
        print("Model saved to: models/web_model_b4.pth")
        print("Confusion matrix saved to: static/images/confusion_matrix.png")
        
    except Exception as e:
        print(f"\nTraining failed: {str(e)}")
        print("Please check your dataset and try again.")
        return

if __name__ == "__main__":
    main()