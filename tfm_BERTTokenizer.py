import os
import json
import numpy as np
import torch
from transformers import AutoTokenizer

# convertint el text del main_body de cada cada json
# en un vector de 768 elements (768 és el nombre de input-features
# de la input layer del BertModel de la llibreria Huggingface)   
# descartant els tokens sobrants (cropping)
# o completant amb zeros (padding)

class BERTTokenizer:
    def __init__(self):
        self.reset()
        print('Loading bert-base-cased tokenizer.')
        self.tknzr = AutoTokenizer.from_pretrained('bert-base-cased')

    def reset(self):
        self.lines = []
        self.tokens = np.array([])
        self.atentionMask = np.zeros(768)

    def tokenize(self, lines):
        self.lines = lines
        for line in self.lines:
            seq = line[:512]
            toks = self.tknzr.tokenize(seq)
            ids = self.tknzr.convert_tokens_to_ids(toks)
            idsNp = np.array(ids)
            self.concatenate(idsNp)
            self.adjustlength()
            tokensTensor = torch.from_numpy(self.tokens)
            attentionMask = torch.from_numpy(self.attentionMask)
            return tokensTensor, attentionMask

    def adjustlength(self):
        self.attentionMask = np.ones(self.tokens.size, dtype = int)
        if self.tokens.size < 768:
            self.padWithZeros()

        if self.tokens.size > 768:
            self.tokens = self.tokens[0:768]
            self.attentionMask = self.attentionMask[0:768] 

    def padWithZeros(self):
        lenPadArray = 768 - self.tokens.size
        padArray = np.zeros(lenPadArray, dtype=int)
        self.tokens = np.concatenate((self.tokens, padArray))
        self.attentionMask = np.concatenate((self.attentionMask, padArray))

    def concatenate(self, idsNp):
        if self.tokens.size > 0:
            self.tokens = np.concatenate((self.tokens, idsNp))
        else:
            self.tokens = idsNp
