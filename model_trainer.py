import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from torchvision import datasets
from efficientnet_pytorch import EfficientNet
import os
from data_preprocessor import DatasetExpander
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

class FocalLoss(nn.Module):
    def __init__(self, alpha=1, gamma=2, reduction='mean'):
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.reduction = reduction
    
    def forward(self, inputs, targets):
        ce_loss = nn.CrossEntropyLoss(reduction='none')(inputs, targets)
        pt = torch.exp(-ce_loss)
        focal_loss = self.alpha * (1-pt)**self.gamma * ce_loss
        
        if self.reduction == 'mean':
            return focal_loss.mean()
        elif self.reduction == 'sum':
            return focal_loss.sum()
        else:
            return focal_loss

class EnhancedTrainer:
    def __init__(self, num_classes=4, model_name='efficientnet-b4'):
        self.num_classes = num_classes
        self.model_name = model_name
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.class_names = ['adenocarcinoma', 'large.cell.carcinoma', 'normal', 'squamous.cell.carcinoma']
        
    def create_model(self):
        """Create EfficientNet-B4 model"""
        model = EfficientNet.from_pretrained('efficientnet-b4')
        model._fc = nn.Linear(model._fc.in_features, self.num_classes)
        return model.to(self.device)
    
    def prepare_data(self, data_dir):
        """Prepare training and validation datasets"""
        expander = DatasetExpander()
        
        train_dataset = datasets.ImageFolder(
            os.path.join(data_dir, 'train'),
            transform=expander.get_training_transforms()
        )
        
        val_dataset = datasets.ImageFolder(
            os.path.join(data_dir, 'valid'),
            transform=expander.get_validation_transforms()
        )
        
        train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True, num_workers=0)
        val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False, num_workers=0)
        
        return train_loader, val_loader
    
    def train_model(self, data_dir, epochs=20, save_path='models/web_model_b4.pth'):
        """Train the EfficientNet-B4 model"""
        model = self.create_model()
        train_loader, val_loader = self.prepare_data(data_dir)
        
        criterion = FocalLoss(alpha=1, gamma=2)
        optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', patience=3, factor=0.5)
        
        best_val_acc = 0.0
        
        for epoch in range(epochs):
            # Training phase
            model.train()
            train_loss = 0.0
            train_correct = 0
            train_total = 0
            
            for batch_idx, (data, target) in enumerate(train_loader):
                data, target = data.to(self.device), target.to(self.device)
                
                optimizer.zero_grad()
                output = model(data)
                loss = criterion(output, target)
                loss.backward()
                optimizer.step()
                
                train_loss += loss.item()
                _, predicted = torch.max(output.data, 1)
                train_total += target.size(0)
                train_correct += (predicted == target).sum().item()
            
            # Validation phase
            model.eval()
            val_loss = 0.0
            val_correct = 0
            val_total = 0
            
            with torch.no_grad():
                for data, target in val_loader:
                    data, target = data.to(self.device), target.to(self.device)
                    output = model(data)
                    loss = criterion(output, target)
                    
                    val_loss += loss.item()
                    _, predicted = torch.max(output.data, 1)
                    val_total += target.size(0)
                    val_correct += (predicted == target).sum().item()
            
            train_acc = 100. * train_correct / train_total
            val_acc = 100. * val_correct / val_total
            
            scheduler.step(val_loss)
            
            print(f'Epoch {epoch+1}/{epochs}:')
            print(f'Train Loss: {train_loss/len(train_loader):.4f}, Train Acc: {train_acc:.2f}%')
            print(f'Val Loss: {val_loss/len(val_loader):.4f}, Val Acc: {val_acc:.2f}%')
            
            if val_acc > best_val_acc:
                best_val_acc = val_acc
                torch.save(model.state_dict(), save_path)
                print(f'Model saved with validation accuracy: {val_acc:.2f}%')
        
        return model
    
    def evaluate_model(self, model_path, data_dir):
        """Evaluate model and generate metrics"""
        model = self.create_model()
        model.load_state_dict(torch.load(model_path, map_location=self.device))
        model.eval()
        
        expander = DatasetExpander()
        test_dataset = datasets.ImageFolder(
            os.path.join(data_dir, 'test'),
            transform=expander.get_validation_transforms()
        )
        test_loader = DataLoader(test_dataset, batch_size=16, shuffle=False)
        
        all_predictions = []
        all_targets = []
        
        with torch.no_grad():
            for data, target in test_loader:
                data = data.to(self.device)
                output = model(data)
                _, predicted = torch.max(output, 1)
                
                all_predictions.extend(predicted.cpu().numpy())
                all_targets.extend(target.numpy())
        
        # Generate confusion matrix
        cm = confusion_matrix(all_targets, all_predictions)
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=self.class_names, yticklabels=self.class_names)
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.tight_layout()
        plt.savefig('static/images/confusion_matrix.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        # Generate classification report
        report = classification_report(all_targets, all_predictions, 
                                     target_names=self.class_names, output_dict=True)
        
        return report, cm