import os
import json
import torch
import torchtext
from torchtext.data.utils import get_tokenizer

class EURLEX57KMainBodySimpleTokensGenerator:
    def __init__(self):
        self.folder_base = 'data/datasets/EURLEX57K/'
        self.folders = ['dev','test','train']
        self.getTokens = self.generator()
        # tokenizer
        self.tokenizer = get_tokenizer('basic_english')


    def generator(self):
        for folder in self.folders:
            print(f'Iterating through folder {folder}')
            full_name_folder = f'{self.folder_base}{folder}'
            for root, _, fullnames in os.walk(full_name_folder):
                for name in fullnames:
                    full_name = f'{full_name_folder}/{name}'
                    fp = open(full_name, 'r')
                    json_file = json.load(fp)
                    main_body = json_file.get('main_body')
                    for part in main_body:
                        lines = part.split('\n')
                        for line in lines:
                            tokens = self.tokenizer(line)
                            yield tokens

    def next(self):
        return next(self.getTokens)
        
        
        
