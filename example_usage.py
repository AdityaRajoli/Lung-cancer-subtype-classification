#!/usr/bin/env python3
"""
Example Usage: Publication-Quality Medical AI Visualizations
Demonstrates how to use the visualization system with real experimental data.

This script shows various ways to integrate your actual research data
with the publication-quality visualization generator.
"""

import numpy as np
from generate_research_visualizations import MedicalAIVisualizer
from data_integration_utils import DataIntegrator
import json

def example_with_real_data():
    """
    Example 1: Using the visualization system with real experimental data.
    Replace the file paths with your actual data files.
    """
    print("Example 1: Using Real Experimental Data")
    print("=" * 50)
    
    # Initialize components
    visualizer = MedicalAIVisualizer()
    integrator = DataIntegrator()
    
    # Method 1: Load data from files (replace with your actual file paths)
    try:
        # Load classification results
        true_labels, predicted_labels = integrator.load_classification_results(
            true_labels_path='your_true_labels.npy',  # Replace with your file
            predicted_labels_path='your_predicted_labels.npy'  # Replace with your file
        )
        
        # Load training history
        training_history = integrator.load_training_history(
            history_path='your_training_history.json'  # Replace with your file
        )
        
        # Load model metrics
        baseline_metrics = integrator.load_model_metrics(
            metrics_path='your_baseline_metrics.json'  # Replace with your file
        )
        
        hybrid_metrics = integrator.load_model_metrics(
            metrics_path='your_hybrid_metrics.json'  # Replace with your file
        )
        
        # Update visualizer with real data
        visualizer.true_labels = true_labels
        visualizer.predicted_labels = predicted_labels
        visualizer.train_accuracy = training_history['train_accuracy']
        visualizer.val_accuracy = training_history['val_accuracy']
        visualizer.train_loss = training_history['train_loss']
        visualizer.val_loss = training_history['val_loss']
        visualizer.baseline_metrics = baseline_metrics
        visualizer.hybrid_metrics = hybrid_metrics
        
        print("✓ Real data loaded successfully!")
        
    except FileNotFoundError:
        print("⚠ Real data files not found. Using sample data instead.")
        # Create sample data for demonstration
        integrator = DataIntegrator()
        from data_integration_utils import create_sample_data_files
        create_sample_data_files()
        
        # Load sample data
        true_labels, predicted_labels = integrator.load_classification_results(
            'sample_true_labels.npy', 'sample_predicted_labels.npy'
        )
        
        visualizer.true_labels = true_labels
        visualizer.predicted_labels = predicted_labels
    
    # Generate all visualizations with real/sample data
    visualizer.generate_all_visualizations()

def example_with_direct_arrays():
    """
    Example 2: Using the visualization system with direct numpy arrays.
    Use this method if you have your data already loaded in memory.
    """
    print("\nExample 2: Using Direct NumPy Arrays")
    print("=" * 50)
    
    # Initialize visualizer
    visualizer = MedicalAIVisualizer()
    
    # Example: Replace these with your actual experimental results
    # Your true labels (ground truth)
    your_true_labels = np.array([0, 1, 2, 3, 0, 1, 2, 3] * 125)  # 1000 samples
    
    # Your model predictions
    your_predicted_labels = np.array([0, 1, 2, 3, 0, 1, 1, 3] * 125)  # Some errors
    
    # Your training history (replace with actual values)
    your_train_accuracy = [0.6 + 0.35 * (1 - np.exp(-0.1 * i)) for i in range(50)]
    your_val_accuracy = [0.55 + 0.37 * (1 - np.exp(-0.1 * i)) for i in range(50)]
    your_train_loss = [1.5 * np.exp(-0.08 * i) + 0.15 for i in range(50)]
    your_val_loss = [1.6 * np.exp(-0.08 * i) + 0.22 for i in range(50)]
    
    # Your model performance metrics
    your_baseline_metrics = {
        'Accuracy': 87.5,
        'Precision': 86.2,
        'Recall': 87.8,
        'F1-Score': 87.0
    }
    
    your_hybrid_metrics = {
        'Accuracy': 93.1,
        'Precision': 92.4,
        'Recall': 93.3,
        'F1-Score': 92.8
    }
    
    # Update visualizer with your data
    visualizer.true_labels = your_true_labels
    visualizer.predicted_labels = your_predicted_labels
    visualizer.train_accuracy = your_train_accuracy
    visualizer.val_accuracy = your_val_accuracy
    visualizer.train_loss = your_train_loss
    visualizer.val_loss = your_val_loss
    visualizer.baseline_metrics = your_baseline_metrics
    visualizer.hybrid_metrics = your_hybrid_metrics
    
    # Calculate class-wise accuracy from your data
    from sklearn.metrics import classification_report
    report = classification_report(your_true_labels, your_predicted_labels, 
                                 target_names=visualizer.class_names, output_dict=True)
    
    visualizer.class_wise_accuracy = {
        name: report[name]['precision'] * 100 
        for name in visualizer.class_names
    }
    
    print("✓ Direct arrays loaded successfully!")
    
    # Generate visualizations with custom prefix
    visualizer.generate_confusion_matrix('custom_confusion_matrix.png')
    visualizer.generate_training_curves('custom_accuracy_curve.png', 'custom_loss_curve.png')
    visualizer.generate_class_wise_accuracy('custom_class_accuracy.png')
    visualizer.generate_model_comparison('custom_model_comparison.png')
    visualizer.generate_gradcam_visualization('custom_gradcam.png')
    
    print("✓ Custom visualizations generated!")

def example_with_string_labels():
    """
    Example 3: Converting string class labels to numeric format.
    Use this if your labels are in string format.
    """
    print("\nExample 3: Converting String Labels")
    print("=" * 50)
    
    # Initialize components
    visualizer = MedicalAIVisualizer()
    integrator = DataIntegrator()
    
    # Example string labels (replace with your actual string labels)
    true_labels_str = ['adenocarcinoma', 'normal', 'squamous.cell.carcinoma', 'large.cell.carcinoma'] * 250
    predicted_labels_str = ['adenocarcinoma', 'normal', 'squamous.cell.carcinoma', 'normal'] * 250
    
    # Convert to numeric format
    true_labels_numeric = integrator.convert_string_labels_to_numeric(true_labels_str)
    predicted_labels_numeric = integrator.convert_string_labels_to_numeric(predicted_labels_str)
    
    # Validate the conversion
    integrator.validate_data_format(true_labels_numeric, predicted_labels_numeric)
    
    # Update visualizer
    visualizer.true_labels = true_labels_numeric
    visualizer.predicted_labels = predicted_labels_numeric
    
    print("✓ String labels converted successfully!")
    
    # Generate confusion matrix with converted labels
    visualizer.generate_confusion_matrix('string_labels_confusion_matrix.png')

def example_custom_configuration():
    """
    Example 4: Customizing the visualization system for specific research needs.
    """
    print("\nExample 4: Custom Configuration")
    print("=" * 50)
    
    # Create custom visualizer with different class names
    class CustomMedicalVisualizer(MedicalAIVisualizer):
        def __init__(self):
            super().__init__()
            # Customize for your specific research
            self.class_names = [
                'Type A Adenocarcinoma',
                'Type B Large Cell',
                'Type C Squamous Cell',
                'Healthy Tissue'
            ]
            
            # Custom colors for your research theme
            self.colors = {
                'primary': '#1f77b4',      # Blue
                'secondary': '#ff7f0e',    # Orange  
                'accent': '#2ca02c',       # Green
                'success': '#d62728',      # Red
                'neutral': '#9467bd',      # Purple
                'background': '#f7f7f7'    # Light gray
            }
    
    # Initialize custom visualizer
    custom_visualizer = CustomMedicalVisualizer()
    
    # Generate with custom settings
    custom_visualizer.generate_confusion_matrix('custom_themed_confusion_matrix.png')
    
    print("✓ Custom configuration applied!")

def example_batch_processing():
    """
    Example 5: Batch processing multiple experiments.
    Use this for comparing multiple model runs or cross-validation results.
    """
    print("\nExample 5: Batch Processing Multiple Experiments")
    print("=" * 50)
    
    # Simulate multiple experimental runs
    experiments = {
        'experiment_1': {'accuracy': 89.2, 'f1': 88.5},
        'experiment_2': {'accuracy': 91.7, 'f1': 90.8},
        'experiment_3': {'accuracy': 93.1, 'f1': 92.4}
    }
    
    visualizer = MedicalAIVisualizer()
    
    for exp_name, metrics in experiments.items():
        print(f"Processing {exp_name}...")
        
        # Update metrics for this experiment
        visualizer.hybrid_metrics['Accuracy'] = metrics['accuracy']
        visualizer.hybrid_metrics['F1-Score'] = metrics['f1']
        
        # Generate visualizations with experiment-specific names
        visualizer.generate_model_comparison(f'{exp_name}_model_comparison.png')
    
    print("✓ Batch processing completed!")

def main():
    """
    Main function demonstrating all usage examples.
    """
    print("Publication-Quality Medical AI Visualizations")
    print("Usage Examples and Integration Guide")
    print("=" * 70)
    
    # Run all examples
    example_with_real_data()
    example_with_direct_arrays()
    example_with_string_labels()
    example_custom_configuration()
    example_batch_processing()
    
    print("\n" + "=" * 70)
    print("INTEGRATION GUIDE SUMMARY:")
    print("=" * 70)
    print("1. For real data files: Use DataIntegrator.load_*() methods")
    print("2. For in-memory arrays: Directly assign to visualizer attributes")
    print("3. For string labels: Use convert_string_labels_to_numeric()")
    print("4. For customization: Subclass MedicalAIVisualizer")
    print("5. For batch processing: Loop with different file names")
    print("\nAll generated figures are publication-ready at 300 DPI!")
    print("Ready for IEEE/Springer journal submission.")

if __name__ == "__main__":
    main()