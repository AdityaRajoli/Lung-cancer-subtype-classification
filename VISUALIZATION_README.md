# Publication-Quality Medical AI Visualizations

**Research Paper:** *A Multi-Modal AI System Integrating CNN-Based Image Analysis with LLM-Powered Medical Reporting for Lung Malignancy*

This repository provides **IEEE/Springer standard** publication-quality visualization tools for medical AI research, specifically designed for lung cancer classification systems using EfficientNet-B4 and hybrid CNN+LLM architectures.

## 🎯 Features

### ✅ **Complete Visualization Suite**
- **Confusion Matrix**: 4-class lung cancer classification with percentages
- **Training Curves**: Accuracy and loss progression with overfitting detection
- **Class-wise Performance**: Bar charts with statistical annotations
- **Model Comparison**: CNN vs. Hybrid CNN+LLM performance
- **Grad-CAM Visualization**: Explainable AI heatmaps for medical interpretation

### ✅ **Publication Standards**
- **300 DPI resolution** for print quality
- **IEEE/Springer formatting** compliance
- **Colorblind-friendly palettes**
- **Professional typography** (Times New Roman)
- **Statistical annotations** and performance metrics
- **Medical-grade disclaimers** and proper labeling

### ✅ **Data Integration**
- Support for **multiple file formats** (.npy, .pkl, .json, .csv, .pt)
- **String-to-numeric** label conversion
- **Real-time data validation**
- **Batch processing** capabilities
- **Custom configuration** options

## 🚀 Quick Start

### 1. Installation

```bash
# Install required packages
pip install -r visualization_requirements.txt

# Or install individually
pip install numpy matplotlib seaborn scikit-learn torch pillow opencv-python
```

### 2. Basic Usage

```python
from generate_research_visualizations import MedicalAIVisualizer

# Initialize visualizer
visualizer = MedicalAIVisualizer()

# Generate all publication-quality figures
visualizer.generate_all_visualizations()
```

### 3. With Your Real Data

```python
from generate_research_visualizations import MedicalAIVisualizer
from data_integration_utils import DataIntegrator

# Load your experimental data
integrator = DataIntegrator()
true_labels, predicted_labels = integrator.load_classification_results(
    'your_true_labels.npy', 'your_predicted_labels.npy'
)

# Initialize and update visualizer
visualizer = MedicalAIVisualizer()
visualizer.true_labels = true_labels
visualizer.predicted_labels = predicted_labels

# Generate figures
visualizer.generate_all_visualizations()
```

## 📊 Generated Visualizations

### 1. Confusion Matrix (`confusion_matrix.png`)
- 4×4 matrix for lung cancer classification
- Shows both counts and percentages
- Medical-friendly color scheme
- Overall accuracy annotation

### 2. Training Curves (`accuracy_curve.png`, `loss_curve.png`)
- Training vs. validation performance
- Overfitting/underfitting detection
- Best performance annotations
- Convergence analysis

### 3. Class-wise Accuracy (`class_wise_accuracy.png`)
- Performance breakdown by cancer type
- Value labels on bars
- Average performance line
- Statistical significance indicators

### 4. Model Comparison (`model_comparison.png`)
- CNN vs. Hybrid CNN+LLM comparison
- Multiple metrics (Accuracy, Precision, Recall, F1)
- Improvement annotations
- Grouped bar visualization

### 5. Grad-CAM Visualization (`gradcam_visualization.png`)
- Explainable AI heatmaps
- CT scan overlay visualization
- Feature attribution analysis
- Medical interpretation support

## 📁 File Structure

```
medical-ai-visualizations/
├── generate_research_visualizations.py  # Main visualization generator
├── data_integration_utils.py           # Data loading utilities
├── example_usage.py                    # Usage examples
├── visualization_requirements.txt      # Package dependencies
├── VISUALIZATION_README.md            # This documentation
└── generated_figures/                 # Output directory
    ├── confusion_matrix.png
    ├── accuracy_curve.png
    ├── loss_curve.png
    ├── class_wise_accuracy.png
    ├── model_comparison.png
    └── gradcam_visualization.png
```

## 🔧 Advanced Usage

### Custom Class Names

```python
class CustomVisualizer(MedicalAIVisualizer):
    def __init__(self):
        super().__init__()
        self.class_names = [
            'Type A Adenocarcinoma',
            'Type B Large Cell',
            'Type C Squamous Cell', 
            'Healthy Tissue'
        ]

visualizer = CustomVisualizer()
```

### Batch Processing

```python
experiments = ['exp1', 'exp2', 'exp3']

for exp in experiments:
    # Load experiment-specific data
    true_labels, pred_labels = load_experiment_data(exp)
    
    # Update visualizer
    visualizer.true_labels = true_labels
    visualizer.predicted_labels = pred_labels
    
    # Generate with custom names
    visualizer.generate_confusion_matrix(f'{exp}_confusion_matrix.png')
```

### String Label Conversion

```python
from data_integration_utils import DataIntegrator

integrator = DataIntegrator()

# Convert string labels to numeric
string_labels = ['adenocarcinoma', 'normal', 'squamous.cell.carcinoma']
numeric_labels = integrator.convert_string_labels_to_numeric(string_labels)
```

## 📋 Data Format Requirements

### Classification Results
- **True Labels**: NumPy array of integers [0, 1, 2, 3]
- **Predicted Labels**: NumPy array of integers [0, 1, 2, 3]
- **Classes**: 0=Adenocarcinoma, 1=Large Cell, 2=Squamous Cell, 3=Normal

### Training History
```python
{
    'train_accuracy': [0.6, 0.7, 0.8, ...],  # List of floats
    'val_accuracy': [0.55, 0.68, 0.79, ...], # List of floats
    'train_loss': [1.5, 1.2, 0.9, ...],      # List of floats
    'val_loss': [1.6, 1.3, 1.0, ...]         # List of floats
}
```

### Model Metrics
```python
{
    'Accuracy': 94.2,    # Float percentage
    'Precision': 93.8,   # Float percentage
    'Recall': 94.0,      # Float percentage
    'F1-Score': 93.9     # Float percentage
}
```

## 🎨 Customization Options

### Color Schemes
```python
# Medical-friendly colors (default)
colors = {
    'primary': '#2E86AB',      # Blue
    'secondary': '#A23B72',    # Magenta
    'accent': '#F18F01',       # Orange
    'success': '#C73E1D',      # Red
    'neutral': '#6C757D'       # Gray
}
```

### Figure Parameters
```python
# Publication settings (automatically applied)
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'axes.labelsize': 14,
    'axes.titlesize': 16
})
```

## 📖 Examples

### Complete Example Scripts

1. **`example_usage.py`** - Comprehensive usage examples
2. **`generate_research_visualizations.py`** - Main generator with dummy data
3. **`data_integration_utils.py`** - Data loading and processing utilities

### Running Examples

```bash
# Generate all visualizations with dummy data
python generate_research_visualizations.py

# Run comprehensive examples
python example_usage.py

# Create sample data files
python data_integration_utils.py
```

## 🔬 Research Integration

### For IEEE/Springer Papers

1. **Figure Quality**: All outputs are 300 DPI, suitable for print publication
2. **Formatting**: Follows academic standards with proper titles and labels
3. **Statistics**: Includes confidence intervals and significance annotations
4. **Reproducibility**: Seed-controlled for consistent results

### Citation Format

```bibtex
@article{your_paper_2024,
    title={A Multi-Modal AI System Integrating CNN-Based Image Analysis with LLM-Powered Medical Reporting for Lung Malignancy},
    author={Your Name and Co-authors},
    journal={IEEE/Springer Journal},
    year={2024},
    note={Visualizations generated using publication-quality medical AI visualization toolkit}
}
```

## ⚠️ Medical Disclaimers

- **Research Use Only**: These visualizations are for research and educational purposes
- **Not Clinical Tools**: Not approved for clinical diagnosis or treatment decisions
- **Professional Review**: All results require qualified medical professional evaluation
- **Validation Required**: Clinical validation needed before medical deployment

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/enhancement`)
3. Commit changes (`git commit -m 'Add enhancement'`)
4. Push to branch (`git push origin feature/enhancement`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For questions or issues:
1. Check the example scripts and documentation
2. Review the data format requirements
3. Ensure all dependencies are installed correctly
4. Verify input data format and ranges

---

**Built for advancing medical AI research with publication-quality standards** 🏥🤖📊