import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'
numInFeatures=512
modelName='distilbert/distilbert-base-uncased'
tknzr = AutoTokenizer.from_pretrained(modelName)

fileIndex = '50LabelsLabelSetFileIndex.txt'

torch.manual_seed(0)


# Load the configuration with the cache directory.
config = AutoConfig.from_pretrained(
    'distilbert-base-uncased',
    force_download=True,
    cache_dir=cache_dir,
    num_labels=labelIndex.numLabels,
    problem_type='multi_label_classification',
    id2label=labelIndex.id2label,
    label2id=labelIndex.label2id
)
