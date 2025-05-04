import numpy as np
import os
import shutil
import torch
from datetime import datetime
from sklearn.metrics import f1_score, roc_auc_score, accuracy_score
from tfm_50LabelsLabelIndex import LabelIndex
from tfm_EURLEX57KDataset import EURLEX57KDataset
from torch.utils.data import random_split
from torch.utils.data import DataLoader
from transformers import AutoConfig, AutoModel
from transformers import TrainingArguments
from transformers import Trainer
from transformers import EvalPrediction

class ModelTrainPipeline:
    def __init__(
            self,
            dataFrameFile,
            modelName,
            modelFile,
            epochNum,
            baseDir = '.',
            metricName = 'f1',
            learning_rate=2e-5,
            weight_decay=0.01):
        self.dataFrameFile = dataFrameFile
        self.modelName = modelName
        self.modelFile = modelFile
        self.epochNum = epochNum
        self.baseDir = baseDir
        self.metricName = metricName
        self.learning_rate = learning_rate
        self.weight_decay=weight_decay
        
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        torch.manual_seed(0)

        self.ds = EURLEX57KDataset(baseDir='.', DataFrameFile=self.dataFrameFile)
        self.fullSetSize = self.ds.__len__()
        self.trainSetSize = int(self.fullSetSize * 0.8)
        self.valSetSize = int(self.fullSetSize * 0.1)
        self.testSetSize = self.fullSetSize - self.trainSetSize - self.valSetSize
        self.trainData, self.valData, self. testData = random_split(
            self.ds,[self.trainSetSize, self.valSetSize, self.testSetSize])
        self.batchSize = 10
        self.trainDataLoader = DataLoader(self.trainData, batch_size=self.batchSize, shuffle=True)
        self.valDataLoader = DataLoader(self.valData, batch_size=self.batchSize, shuffle=True)
        self.testDataLoader = DataLoader(self.testData, batch_size=self.batchSize, shuffle=True)

        self.labelIndex = LabelIndex(self.baseDir)

        self.cache_dir = os.path.join(self.baseDir, 'tfm_cache')
        os.makedirs(self.cache_dir, exist_ok=True)
        self.config = AutoConfig.from_pretrained(
            self.modelName,
            force_download=True,
            cache_dir=self.cache_dir,
            num_labels=self.labelIndex.numLabels,
            problem_type='multi_label_classification',
            id2label=self.labelIndex.id2label,
            label2id=self.labelIndex.label2id
        )

        if self.epochNum == 1:
            self.model = AutoModel.from_pretrained(
                self.modelName,
                config=self.config,
                cache_dir=self.cache_dir
            )
        else:
            self.model = torch.load(os.path.join(self.baseDir, self.modelFile), map_location=torch.device(self.device))

        self.trainArgs = TrainingArguments(
            'tfm_oputput',
            report_to = 'none',
            evaluation_strategy = 'epoch',
            save_strategy = 'epoch',
            learning_rate = self.learning_rate,
            per_device_train_batch_size = self.batchSize,
            per_device_eval_batch_size = self.batchSize,
            num_train_epochs = 1,
            weight_decay = self.weight_decay,
            load_best_model_at_end = True,
            metric_for_best_model=self.metricName
        )

        self.trainer = Trainer(
            model=self.model,
            args=self.trainArgs,
            train_dataset=self.trainData,
            eval_dataset=self.valData,
            compute_metrics = self.compute_metrics
        )

    def countNonZeroItems(self, items):
        nonZero = torch.nonzero(items, as_tuple= True)
        return len(nonZero[0])

    def multi_label_metrics(self, predictions, labels, ):
        sigmoid = torch.nn.Sigmoid()
        probs = sigmoid(torch.Tensor(predictions))
        y_pred = np.zeros(probs.shape)
        y_true = labels
        y_pred[np.where(probs >= 0.5)] = 1
        f1_micro_average = f1_score(y_true=y_true, y_pred=y_pred, average='micro')
        roc_auc = roc_auc_score(y_true, y_pred, average = 'micro')
        accuracy = accuracy_score(y_true, y_pred)

        metrics = {
            'f1': f1_micro_average,
            'roc_auc': roc_auc,
            'accuracy': accuracy
        }

        return metrics

    def compute_metrics(self, p: EvalPrediction):
        preds = p.predictions[0] if isinstance(p.predictions, tuple) else p.predictions
        result = self.multi_label_metrics(
            predictions=preds,
            labels=p.label_ids)

        return result

    def metricsForTestSet(self):
        predictions = self.trainer.predict(self.testData)
        preds = predictions.predictions[0] if isinstance(predictions.predictions, tuple) else predictions.predictions
        labels = predictions.label_ids
        testMetrics = self.multi_label_metrics(predictions=preds, labels=labels)

        print(testMetrics)

    def trainingPipeline(self):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        # Move the model to the correct device before training.
        self.model.to(device)

        # baseline
        print(f'Begin epoch {self.epochNum} train session - trainer evaluate')
        self.trainer.evaluate()

        print('Metrics for test set (before train)')
        self.metricsForTestSet()

        # training
        print('Epoch train.')

        self.trainer.train()
        print('Epoch train done.')

        # evaluate epoch training
        print('End epoch train session - trainer evaluate')
        self.trainer.evaluate()

        print('Metrics for test set (after train)')
        self.metricsForTestSet()

        print('End epoch train session')

    def saveEpochTraining(self, modelName, folderGDrive = '/content/drive/MyDrive/TFM-MUECIM'):
        prefixDate = datetime.today().strftime('%Y%m%d')
        fileName = f'{prefixDate}_50L_{modelName}_epoch_{self.epochNum}.pt'
        modelFullPath = os.path.join(baseDir,fileName)
        destFullPath = os.path.join(folderGDrive,fileName)

        print(f'Saving model "{modelName}" after epoch {self.epochNum} train session')
        print(f'file name: {fileName}')
        print(f'full path: {modelFullPath}')
        print(f'full path (copy): {destFullPath}')
        torch.save(self.model, modelFullPath)
        shutil.copyfile(modelFullPath, destFullPath)
        print('Done!')
