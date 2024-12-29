import os
import json
import numpy as np
import torch
from tfm_BERTUtils import BERTTokenizer

# itera pel sets (dev, test, train)
# convertint el text del main_body de cada cada json
# en un vector de 768 elements (768 és el nombre de input-features
# de la input layer del BertModel de la llibreria Huggingface)   
# descartant els tokens sobrants (cropping)
# o completant amb zeros (padding)

class BasicPreprocesssor:
    def __init__(self):
        self.folderBase = 'data/datasets/EURLEX57K/'
        self.folders = ['dev','test','train']
        tknzr = BERTTokenizer()
        fdErr = open(f'{self.folderBase}/errors.txt', 'w')
        
        for folder in self.folders:
            print(f'Iterating through folder {folder}')
            fullNameFolder = f'{self.folderBase}{folder}'
            for root, _, fullnames in os.walk(fullNameFolder):
                for name in fullnames:
                    fullName = f'{fullNameFolder}/{name}'
                    fp = open(fullName, 'r')
                    try:
                        jsonFile = json.load(fp)
                        mainBody = jsonFile.get('main_body')
                    except Exception as ex:
                        fdErr.write(f'full name: {fullName}')
                        mainBody = ''
                    fp.close()

                    self.tokens = np.array([])
                    for part in mainBody:
                        lines = part.split('\n')
                        for line in lines:
                            seq = line[:512]
                            toks = tknzr.tokenizer.tokenize(seq)
                            ids = tknzr.tokenizer.convert_tokens_to_ids(toks)
                            idsNp = np.array(ids)
                            self.concatenate(idsNp)

                    self.adjustlength()

                    self.save(fullName)

        fdErr.close()

    def adjustlength(self):
        if self.tokens.size < 768:
            self.padWithZeros()

        if self.tokens.size > 768:
            self.tokens = self.tokens[0:768]

    def padWithZeros(self):
        lenPadArray = 768 - self.tokens.size
        padArray = np.zeros(lenPadArray, dtype=int)
        self.tokens = np.concatenate((self.tokens, padArray))


    def concatenate(self, idsNp):
        if self.tokens.size > 0:
            self.tokens = np.concatenate((self.tokens, idsNp))
        else:
            self.tokens = idsNp

    def save(self, fileName):
        vectorFileName = f'{fileName}.tensor'
        tokensTensor = torch.from_numpy(self.tokens)
        torch.save(tokensTensor, vectorFileName)

if __name__ == '__main__':
    print('Init')
    BasicPreprocesssor()
    print('Done!')
