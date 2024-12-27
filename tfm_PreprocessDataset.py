import re
import os
import json
import numpy as np
import pandas as pd
from tfm_BERTutils import BERTTokenizer

# itera pel sets (dev, test, train)
# convertint el text del main_body de cada cada json
# en un vector de 768 elements,
# descartant els tokens sobrants (cropping)
# o completant amb zeros (padding)

class BasicPreprocesssor:
    def __init__(self):
        self.folderBase = 'data/datasets/EURLEX57K/'
        self.folders = ['dev','test','train']
        tknzr = BERTTokenizer()
        
        for folder in self.folders:
            print(f'Iterating through folder {folder}')
            fullNameFolder = f'{self.folderBase}{folder}'
            for root, _, fullnames in os.walk(fullNameFolder):
                for name in fullnames:
                    fullName = f'{fullNameFolder}/{name}'
                    fp = open(fullName, 'r')
                    jsonFile = json.load(fp)
                    mainBody = jsonFile.get('main_body')
                    fp.close()

                    tokens = np.array([])
                    for part in mainBody:
                        lines = part.split('\n')
                        for line in lines:
                            toks = tknzr.tokenizer.tokenize(line)
                            ids = tknzr.tokenizer.convert_tokens_to_ids(toks)
                            idsNp = np.array(ids)
                            self.tokens = np.concatenate((self.tokens, idsNp))

                    if len(self.tokens) < 768:
                        self.tokens = self.padWithZeros()

                    if len(self.tokens) > 768:
                        self.tokens = self.tokens[0:768]

                    self.save(fullName)

    def padWithzeros(self):
        # TODO
        None

    def save(self, fileName):
        # TODO
        None
