import os
import json
import numpy as np
from transformers import AutoTokenizer

# convertint el text del main_body de cada cada json
# en un vector de 512 elements (mida de l' input layer del model de la llibreria Huggingface)   
# descartant els tokens sobrants (cropping)
# o completant amb zeros (padding)

class BERTTokensBuilder:
    def __init__(self):
        self.numInFeatures = 512
        self.reset()
        print('Loading distilbert-base-uncased tokenizer.')
        self.tknzr = AutoTokenizer.from_pretrained('distilbert-base-uncased')

    def reset(self):
        self.lines = []
        self.tokens = np.array([])
        self.atentionMask = np.zeros(self.numInFeatures) #768

    def tokenize(self, lines):
        self.lines = lines
        for line in self.lines:
            seq = line[:self.numInFeatures]
            toks = self.tknzr.tokenize(seq)
            ids = self.tknzr.convert_tokens_to_ids(toks)
            idsNp = np.array(ids)
            self.concatenate(idsNp)
            self.adjustlength()
            return self.tokens, self.attentionMask

    def adjustlength(self):
        self.attentionMask = np.ones(self.tokens.size, dtype = int)
        if self.tokens.size < self.numInFeatures: #768
            self.padWithZeros()

        if self.tokens.size > self.numInFeatures: # 768
            self.tokens = self.tokens[0:self.numInFeatures] #768
            self.attentionMask = self.attentionMask[0:self.numInFeatures]  #768

    def padWithZeros(self):
        lenPadArray = self.numInFeatures - self.tokens.size  # 768
        padArray = np.zeros(lenPadArray, dtype=int)
        self.tokens = np.concatenate((self.tokens, padArray))
        self.attentionMask = np.concatenate((self.attentionMask, padArray))

    def concatenate(self, idsNp):
        if self.tokens.size > 0:
            self.tokens = np.concatenate((self.tokens, idsNp))
        else:
            self.tokens = idsNp