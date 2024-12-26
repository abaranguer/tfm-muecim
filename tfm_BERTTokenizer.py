import torch
from transformers import AutoTokenizer, AutoModel
#from datasets import load_dataset

# https://huggingface.co/docs/transformers/en/training

class BERTTokenizer:
    def __init__(self, ):
        print('Loading bert-base-cased.')
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")


if __name__ == '__main__':
    bertTknzr = BERTTokenizer()
    toks = bertTknzr.tokenizer.tokenize('this is a test')
    ids = bertTknzr.tokenizer.convert_tokens_to_ids(toks)
    print(f'toks: {toks}')
    print(f'ids: {ids}')
    
    
    
