import torch
from transformers import AutoTokenizer, AutoModel
#from datasets import load_dataset

# https://huggingface.co/docs/transformers/en/training

class BERTTokenizer:
    def __init__(self, ):
        print('Loading bert-base-cased.')
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")

    
    
