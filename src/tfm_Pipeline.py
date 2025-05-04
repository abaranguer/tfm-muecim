import os
import torch
from tfm_LabelLoader import LabelLoader
from tfm_EURLEX57KDataset import EURLEX57KDataset
from torch.utils.data import DataLoader, random_split
from transformers import AutoModelForSequenceClassification
from transformers import TrainingArguments, Trainer
from transformers import EvalPrediction
from sklearn.metrics import f1_score, roc_auc_score, accuracy_score
 
def countNonZeroLabels(items):
    nonZero = torch.nonzero(items, as_tuple= True)
    return len(nonZero[0])

# source: https://jesusleal.io/2021/04/21/Longformer-multilabel-classification/
def multi_label_metrics(predictions, labels, threshold=0.5):
    # first, apply sigmoid on predictions which are of shape
    # (batch_size, num_labels)
    sigmoid = torch.nn.Sigmoid()
    probs = sigmoid(torch.Tensor(predictions))
    # next, use threshold to turn them into integer predictions
    y_pred = np.zeros(probs.shape)
    y_pred[np.where(probs >= threshold)] = 1
    # finally, compute metrics
    y_true = labels
    f1_micro_average = f1_score(y_true=y_true, y_pred=y_pred, average='micro')
    roc_auc = roc_auc_score(y_true, y_pred, average = 'micro')
    accuracy = accuracy_score(y_true, y_pred)
    # return as dictionary
    metrics = {'f1': f1_micro_average,
               'roc_auc': roc_auc,
               'accuracy': accuracy}
    return metrics

def compute_metrics(p: EvalPrediction):
    preds = p.predictions[0] if isinstance(p.predictions, 
            tuple) else p.predictions
    result = multi_label_metrics(
        predictions=preds, 
        labels=p.label_ids)
    return result

# Fine-tuning BERT (and friends) for multi-label text classification.ipynb
# https://colab.research.google.com/github/NielsRogge/Transformers-Tutorials
# /blob/master/BERT/
# Fine_tuning_BERT_(and_friends)_for_multi_label_text_classification.ipynb
# #scrollTo=HgpKXDfvKBxn

if __name__ == '__main__':
    os.system("clear")
    print('Test pipeline\n')

    baseDir = '/content/drive/My Drive/TFM-MUECIM'
    # sys.path.append(baseDir)
    
    # ensures reproducibility
    torch.manual_seed(0)

    # load labels
    labelLoader = LabelLoader(baseDir)
    
    # create train, val and test datasets
    indexFile = 'FilesIndex.txt'
    ds = EURLEX57KDataset(baseDir, indexFile)
    trainData, valData, testData = random_split(ds, [45000, 6000, 6000])

    # set batch size
    batchSize = 10
    
    # create dataloaders
    #trainDataLoader = DataLoader(trainData, batch_size=batchSize, shuffle=True)
    #valDataLoader = DataLoader(valData, batch_size=batchSize, shuffle=True)
    #testDataLoader = DataLoader(testData, batch_size=batchSize, shuffle=True)

    # bert huggingface pretrained model 
    model = AutoModelForSequenceClassification.from_pretrained(
        "bert-base-cased", 
        problem_type="multi_label_classification", 
        num_labels=len(labelLoader.labels))

    #,
    #    id2label=id2label,
    #    label2id=label2id)

    # metric
    metricName = 'f1'

    # training arguments
    args = TrainingArguments(
        f'bert-finetuned-sem_eval-english',
        evaluation_strategy = 'epoch',
        save_strategy = 'epoch',
        learning_rate=2e-5,
        per_device_train_batch_size=batchSize,
        per_device_eval_batch_size=batchSize,
        num_train_epochs=5,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model=metricName,
    )

    #forward pass
    #outputs = model(
    #    input_ids=encoded_dataset['train']['input_ids'][0].unsqueeze(0),
    #    labels=encoded_dataset['train'][0]['labels'].unsqueeze(0))

    
    outputs = model(
        input_ids=train_data.unsqueeze(0),
        labels=encoded_datasettrain_data['train'][0]['labels'].unsqueeze(0))


    trainer = Trainer(
        model,
        args,
        train_dataset=encoded_dataset["train"],
        eval_dataset=encoded_dataset["validation"],
        tokenizer=tokenizer,
        compute_metrics=compute_metrics
    )

    # train
    trainer.train()

    # evaluate
    trainer.evaluate()

    # inference
    text = "I'm happy I can finally train a model for multi-label classification"
    encoding = tokenizer(text, return_tensors="pt")
    encoding = {k: v.to(trainer.model.device) for k,v in encoding.items()}
    outputs = trainer.model(**encoding)
    logits = outputs.logits
    print(f'logits.shape: {logits.shape}')

    # apply sigmoid + threshold
    sigmoid = torch.nn.Sigmoid()
    probs = sigmoid(logits.squeeze().cpu())
    predictions = np.zeros(probs.shape)
    predictions[np.where(probs >= 0.5)] = 1
    # turn predicted id's into actual label names
    predicted_labels = [id2label[idx]
                        for idx, label in enumerate(predictions)
                        if label == 1.0]
    print(predicted_labels)

    '''
    # iterate through val batches
    for i, batch in enumerate(valDataLoader):
        print(f'Batch {i}: ')
        batchFileNames = batch.get('fileName')
        batchData = batch.get('data')
        batchLabels = batch.get('labels')

        for elem in zip(batchFileNames, batchData, batchLabels):
            print(f'fileName: {elem[0]}')
            print(f'data (5 first elements):\n{elem[1][0:5]}')
            print(f'Nonzero labels:{countNonZeroLabels(elem[2])}\n')         

    print('Done!')
    '''
