import torch
from transformers import AutoTokenizer, AutoModel
from datasets import load_dataset

# https://huggingface.co/docs/transformers/en/training

class CustomTokenizer:
    def __init__(self):
        print('Building tokens...')

        tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
        model = AutoModel.from_pretrained("bert-base-cased")

        print('Tokenization done.')

    
