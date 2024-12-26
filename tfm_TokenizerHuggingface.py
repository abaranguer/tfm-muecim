import torch
from transformers import AutoTokenizer
from datasets import load_dataset

# https://huggingface.co/docs/transformers/en/training


class Tokenizator(self):
    def __init__():
        print('Building tokens...')

        tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
        dataset = dataset.map(lambda examples: tokenizer(examples["text"]), batched=True)



        print('Tokenization done.')

    
