import matplotlib.pyplot as plt
import numpy as np

# Cancer types and their accuracy (using precision as proxy from README)
cancer_types = ['Adenocarcinoma', 'Large Cell\nCarcinoma', 'Normal', 'Squamous Cell\nCarcinoma']
accuracies = [92.1, 87.3, 98.7, 85.4]

# Create bar plot
plt.figure(figsize=(10, 6))
bars = plt.bar(cancer_types, accuracies, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])

# Customize plot
plt.title('EfficientNet-B4+GPT-3.5', fontsize=16, fontweight='bold')
plt.ylabel('Accuracy (%)', fontsize=12)
plt.xlabel('Cancer Types', fontsize=12)
plt.ylim(0, 100)

# Add value labels on bars
for bar, acc in zip(bars, accuracies):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
             f'{acc}%', ha='center', va='bottom', fontweight='bold')

# Grid and styling
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()

# Save and show
plt.savefig('cancer_accuracy_barplot.png', dpi=300, bbox_inches='tight')
plt.show()