import os
import torch
from .tfm_Classifier import Classifier
from .tfm_EURLEX57KDataset import EURLEX57KDataset
from .tfm_50LabelsLabelIndex import LabelIndex
from transformers import BertModel

class BERTClassifier(Classifier):
    def __init__(self):
        super().__init__()
        self.ds = EURLEX57KDataset(self.baseDir,'csv/TokenizedBERTDataFrame.csv')
        self.modelFile = '20250216_50L_tfm_BERT_model_epoch_6.pt'

        torch.serialization.add_safe_globals([BertModel])
        self.model = torch.load(
            os.path.join(self.modelFolder, self.modelFile),
            map_location=torch.device(self.device),
            weights_only=False)
