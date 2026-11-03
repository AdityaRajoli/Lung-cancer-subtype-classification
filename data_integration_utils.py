#!/usr/bin/env python3
"""
Data Integration Utilities for Medical AI Visualization
Handles real data loading and preprocessing for publication visualizations.

This module provides utilities to integrate real experimental data with the visualization system.
"""

import numpy as np
import pandas as pd
import torch
import pickle
from typing import Dict, List, Tuple, Optional, Union
import json
from pathlib import Path

class DataIntegrator:
    """
    Utility class for integrating real experimental data with visualization system.
    Supports various data formats commonly used in medical AI research.
    """
    
    def __init__(self):
        """Initialize the data integrator."""
        self.supported_formats = ['.npy', '.pkl', '.json', '.csv', '.pt', '.pth']
    
    def load_classification_results(self, 
                                  true_labels_path: Optional[str] = None,
                                  predicted_labels_path: Optional[str] = None,
                                  true_labels: Optional[np.ndarray] = None,
                                  predicted_labels: Optional[np.ndarray] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Load classification results from files or arrays.
        
        Args:
            true_labels_path: Path to true labels file
            predicted_labels_path: Path to predicted labels file  
            true_labels: Direct array of true labels
            predicted_labels: Direct array of predicted labels
            
        Returns:
            Tuple of (true_labels, predicted_labels) as numpy arrays
        """
        if true_labels is not None and predicted_labels is not None:
            return np.array(true_labels), np.array(predicted_labels)
        
        if true_labels_path and predicted_labels_path:
            true_labels = self._load_array_data(true_labels_path)
            predicted_labels = self._load_array_data(predicted_labels_path)
            return true_labels, predicted_labels
        
        raise ValueError("Must provide either file paths or direct arrays for labels")
    
    def load_training_history(self, 
                            history_path: Optional[str] = None,
                            history_dict: Optional[Dict] = None) -> Dict[str, List[float]]:
        """
        Load training history from file or dictionary.
        
        Args:
            history_path: Path to training history file
            history_dict: Direct dictionary with training history
            
        Returns:
            Dictionary with training metrics
        """
        if history_dict is not None:
            return history_dict
        
        if history_path:
            return self._load_dict_data(history_path)
        
        raise ValueError("Must provide either history file path or dictionary")
    
    def load_model_metrics(self,
                          metrics_path: Optional[str] = None,
                          metrics_dict: Optional[Dict] = None) -> Dict[str, float]:
        """
        Load model performance metrics.
        
        Args:
            metrics_path: Path to metrics file
            metrics_dict: Direct dictionary with metrics
            
        Returns:
            Dictionary with performance metrics
        """
        if metrics_dict is not None:
            return metrics_dict
        
        if metrics_path:
            return self._load_dict_data(metrics_path)
        
        raise ValueError("Must provide either metrics file path or dictionary")
    
    def _load_array_data(self, file_path: str) -> np.ndarray:
        """Load array data from various file formats."""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        suffix = path.suffix.lower()
        
        if suffix == '.npy':
            return np.load(file_path)
        elif suffix == '.pkl':
            with open(file_path, 'rb') as f:
                return pickle.load(f)
        elif suffix in ['.pt', '.pth']:
            return torch.load(file_path).numpy()
        elif suffix == '.csv':
            return pd.read_csv(file_path).values.flatten()
        elif suffix == '.json':
            with open(file_path, 'r') as f:
                data = json.load(f)
                return np.array(data)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")
    
    def _load_dict_data(self, file_path: str) -> Dict:
        """Load dictionary data from various file formats."""
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        suffix = path.suffix.lower()
        
        if suffix == '.json':
            with open(file_path, 'r') as f:
                return json.load(f)
        elif suffix == '.pkl':
            with open(file_path, 'rb') as f:
                return pickle.load(f)
        elif suffix == '.csv':
            df = pd.read_csv(file_path)
            return df.to_dict('list')
        else:
            raise ValueError(f"Unsupported file format for dictionary: {suffix}")
    
    def validate_data_format(self, 
                           true_labels: np.ndarray, 
                           predicted_labels: np.ndarray,
                           num_classes: int = 4) -> bool:
        """
        Validate that the data format is correct for visualization.
        
        Args:
            true_labels: Array of true class labels
            predicted_labels: Array of predicted class labels
            num_classes: Expected number of classes
            
        Returns:
            True if data format is valid
        """
        # Check array shapes
        if true_labels.shape != predicted_labels.shape:
            raise ValueError("True and predicted labels must have same shape")
        
        # Check label ranges
        if np.min(true_labels) < 0 or np.max(true_labels) >= num_classes:
            raise ValueError(f"True labels must be in range [0, {num_classes-1}]")
        
        if np.min(predicted_labels) < 0 or np.max(predicted_labels) >= num_classes:
            raise ValueError(f"Predicted labels must be in range [0, {num_classes-1}]")
        
        return True
    
    def convert_string_labels_to_numeric(self, 
                                       labels: Union[List[str], np.ndarray],
                                       class_mapping: Optional[Dict[str, int]] = None) -> np.ndarray:
        """
        Convert string class labels to numeric format.
        
        Args:
            labels: Array or list of string labels
            class_mapping: Optional mapping from strings to integers
            
        Returns:
            Numeric array of class labels
        """
        if class_mapping is None:
            # Default mapping for lung cancer classes
            class_mapping = {
                'adenocarcinoma': 0,
                'large.cell.carcinoma': 1,
                'large_cell_carcinoma': 1,
                'squamous.cell.carcinoma': 2,
                'squamous_cell_carcinoma': 2,
                'normal': 3
            }
        
        # Convert to lowercase for matching
        labels_lower = [str(label).lower() for label in labels]
        
        # Map to numeric values
        numeric_labels = []
        for label in labels_lower:
            if label in class_mapping:
                numeric_labels.append(class_mapping[label])
            else:
                raise ValueError(f"Unknown class label: {label}")
        
        return np.array(numeric_labels)
    
    def save_processed_data(self, 
                          data: Dict, 
                          save_path: str = 'processed_visualization_data.pkl'):
        """
        Save processed data for later use.
        
        Args:
            data: Dictionary containing all processed data
            save_path: Path to save the processed data
        """
        with open(save_path, 'wb') as f:
            pickle.dump(data, f)
        print(f"✓ Processed data saved to {save_path}")
    
    def load_processed_data(self, load_path: str = 'processed_visualization_data.pkl') -> Dict:
        """
        Load previously processed data.
        
        Args:
            load_path: Path to load the processed data from
            
        Returns:
            Dictionary containing processed data
        """
        with open(load_path, 'rb') as f:
            data = pickle.load(f)
        print(f"✓ Processed data loaded from {load_path}")
        return data


def create_sample_data_files():
    """
    Create sample data files for demonstration purposes.
    This function generates realistic sample data in various formats.
    """
    print("Creating sample data files for demonstration...")
    
    # Set random seed for reproducibility
    np.random.seed(42)
    
    # Generate sample classification results
    n_samples = 1000
    true_labels = np.random.choice(4, n_samples, p=[0.3, 0.2, 0.25, 0.25])
    predicted_labels = true_labels.copy()
    # Add some misclassifications
    noise_indices = np.random.choice(n_samples, int(n_samples * 0.08), replace=False)
    predicted_labels[noise_indices] = np.random.choice(4, len(noise_indices))
    
    # Save in different formats
    np.save('sample_true_labels.npy', true_labels)
    np.save('sample_predicted_labels.npy', predicted_labels)
    
    # Create training history
    epochs = 50
    history = {
        'train_accuracy': np.random.uniform(0.6, 0.95, epochs).tolist(),
        'val_accuracy': np.random.uniform(0.55, 0.92, epochs).tolist(),
        'train_loss': np.random.uniform(0.15, 1.5, epochs)[::-1].tolist(),
        'val_loss': np.random.uniform(0.22, 1.6, epochs)[::-1].tolist()
    }
    
    with open('sample_training_history.json', 'w') as f:
        json.dump(history, f, indent=2)
    
    # Create model metrics
    baseline_metrics = {
        'accuracy': 89.3,
        'precision': 88.7,
        'recall': 89.1,
        'f1_score': 88.9
    }
    
    hybrid_metrics = {
        'accuracy': 94.2,
        'precision': 93.8,
        'recall': 94.0,
        'f1_score': 93.9
    }
    
    with open('sample_baseline_metrics.json', 'w') as f:
        json.dump(baseline_metrics, f, indent=2)
    
    with open('sample_hybrid_metrics.json', 'w') as f:
        json.dump(hybrid_metrics, f, indent=2)
    
    print("✓ Sample data files created:")
    print("  • sample_true_labels.npy")
    print("  • sample_predicted_labels.npy")
    print("  • sample_training_history.json")
    print("  • sample_baseline_metrics.json")
    print("  • sample_hybrid_metrics.json")


if __name__ == "__main__":
    # Create sample data files for demonstration
    create_sample_data_files()
    
    # Demonstrate data integration
    integrator = DataIntegrator()
    
    # Load sample data
    true_labels, predicted_labels = integrator.load_classification_results(
        'sample_true_labels.npy', 'sample_predicted_labels.npy'
    )
    
    history = integrator.load_training_history('sample_training_history.json')
    baseline_metrics = integrator.load_model_metrics('sample_baseline_metrics.json')
    hybrid_metrics = integrator.load_model_metrics('sample_hybrid_metrics.json')
    
    # Validate data
    integrator.validate_data_format(true_labels, predicted_labels)
    
    print("\n✓ Data integration demonstration completed successfully!")