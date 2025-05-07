import json
import numpy as np
import os
import torch
from sklearn.metrics import f1_score, roc_auc_score, accuracy_score
from .tfm_EURLEX57KDataset import EURLEX57KDataset
from .tfm_50LabelsLabelIndex import LabelIndex


class Classifier:
    def __init__(self):
        self.baseDir = '/content/tfm_www'
        datFolder = f'{self.baseDir}/dat'
        self.labelIndex = LabelIndex(datFolder)
        self.modelFolder = '/content/tfm_www/models'
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.model = None
        self.ds = None

    def predict(self, idDataFrame):
        item = self.ds.__getitem__(idDataFrame)
        outputs = self.model(
            input_ids=item['input_ids'][0:512].unsqueeze(0),
            attention_mask=item['attention_mask'][0:512].unsqueeze(0),
            labels=item['labels'].unsqueeze(0))

        sigmoid = torch.nn.Sigmoid()
        probs = sigmoid(outputs.logits[0])
        threshold = 0.5
        y_pred = np.zeros(probs.shape)
        y_pred[np.where(probs >= threshold)] = 1
        y_true = item['labels'].cpu().numpy()

        f1_micro_average = f1_score(y_true=y_true, y_pred=y_pred, average='micro')
        roc_auc = roc_auc_score(y_true, y_pred, average = 'micro')
        accuracy = accuracy_score(y_true, y_pred)

        metrics = {
            'f1': f1_micro_average,
            'roc_auc': roc_auc,
            'accuracy': accuracy
        }

        answer = []
        i = 0
        for y in zip(y_true, y_pred):
            if y[0] == 1 and y[1] == 1:
                answer.append(f'Correcte: {self.labelIndex.id2label[i]}')
            if y[0] != y[1]:
                if y[0] == 1:
                    answer.append(f'Error: ground truth: {self.labelIndex.id2label[i]}, però no predit.')
                else:
                    answer.append(f'Error: predit: {self.labelIndex.id2label[i]}, però no al ground truth.')
            i += 1

        jsonResponse = json.dumps(answer)

        return jsonResponse
