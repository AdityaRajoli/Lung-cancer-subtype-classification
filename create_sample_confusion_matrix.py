#!/usr/bin/env python3
"""
Create a sample confusion matrix for demonstration purposes
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

def create_sample_confusion_matrix():
    """Create a sample confusion matrix for the 4 lung cancer classes"""
    
    # Sample confusion matrix data (simulated high-performance results)
    # Rows: True labels, Columns: Predicted labels
    confusion_matrix = np.array([
        [89, 3, 2, 1],   # Adenocarcinoma
        [2, 47, 1, 0],   # Large Cell Carcinoma  
        [1, 0, 48, 1],   # Normal
        [3, 2, 1, 79]    # Squamous Cell Carcinoma
    ])
    
    class_names = ['Adenocarcinoma', 'Large Cell\nCarcinoma', 'Normal', 'Squamous Cell\nCarcinoma']
    
    # Create the plot
    plt.figure(figsize=(10, 8))
    sns.heatmap(confusion_matrix, 
                annot=True, 
                fmt='d', 
                cmap='Blues',
                xticklabels=class_names,
                yticklabels=class_names,
                cbar_kws={'label': 'Number of Samples'})
    
    plt.title('Confusion Matrix - Lung Cancer Classification\n(EfficientNet-B4 Model)', 
              fontsize=16, fontweight='bold', pad=20)
    plt.ylabel('True Label', fontsize=14, fontweight='bold')
    plt.xlabel('Predicted Label', fontsize=14, fontweight='bold')
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    plt.yticks(rotation=0)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Create directory if it doesn't exist
    os.makedirs('static/images', exist_ok=True)
    
    # Save the plot
    plt.savefig('static/images/confusion_matrix.png', 
                dpi=300, 
                bbox_inches='tight',
                facecolor='white',
                edgecolor='none')
    
    plt.close()
    
    print("Sample confusion matrix created and saved to: static/images/confusion_matrix.png")

if __name__ == "__main__":
    create_sample_confusion_matrix()