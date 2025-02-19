from logging import raiseExceptions
import torch 
import torch.nn as nn
import torchvision

class ClsModel(nn.Module):
    def __init__(self, model_name, num_classes, dropout=0, is_pretrained=False):
        super(ClsModel, self).__init__()
        self.model_name = model_name
        self.num_class = num_classes
        self.is_pretrained = is_pretrained
        self.dropout = dropout
        
        self.base_model = getattr(torchvision.models, self.model_name)(self.is_pretrained == True)
        if hasattr(self.base_model, 'classifier'):
            self.base_model.last_layer_name = 'classifier'
            feature_dim = self.base_model.classifier[1].in_features
        elif hasattr(self.base_model, 'fc'):
            self.base_model.last_layer_name = 'fc'
            feature_dim = getattr(self.base_model, self.base_model.last_layer_name).in_features
            setattr(self.base_model, self.base_model.last_layer_name, nn.Dropout(p=self.dropout))
        else:
            raiseExceptions('Please confirm the name of last')
        
        self.new_fc = nn.Linear(feature_dim, self.num_class)


    def forward(self, x):
        x = self.base_model(x)
        x = self.new_fc(x)
        return x

    
if __name__ == '__main__':
    model_name = 'resnet50'
    num_classes = 2
    is_pretrained = False
    
    clsmodel = ClsModel(model_name, num_classes, 0, is_pretrained)
    print(clsmodel)