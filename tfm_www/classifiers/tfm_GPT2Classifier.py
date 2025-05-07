import os
import torch
from .tfm_Classifier import Classifier
from .tfm_EURLEX57KDataset import EURLEX57KDataset
from .tfm_50LabelsLabelIndex import LabelIndex
from transformers import GPT2Model

class GPT2Classifier(Classifier):
    def __init__(self):
        super().__init__()
        self.ds = EURLEX57KDataset(self.baseDir,'csv/TokenizedGPT2DataFrame.csv')
        self.modelFile = '20250322_50L_gpt2_epoch_5.pt'

        torch.serialization.add_safe_globals([GPT2Model])
        self.model = torch.load(os.path.join(
            self.modelFolder, self.modelFile),
            map_location=torch.device(self.device),
            weights_only=False)

