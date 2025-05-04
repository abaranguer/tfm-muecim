import os
import json
import numpy as np
from transformers import GPT2Tokenizer

class GPT2TokensBuilder:
    def __init__(self, numInFeatures=512):
        self.numInFeatures = 512
        self.modelName = 'GPT2'
        self.reset()
        print(f'Loading "GPT2" tokenizer.')
        self.tknzr = GPT2Tokenizer.from_pretrained(
            pretrained_model_name_or_path=self.modelName)
        self.tknzr.padding_side = "left"
        self.tknzr.pad_token = self.tknzr.eos_token

    def reset(self):
        self.lines = []
        self.tokens = np.array([])
        self.atentionMask = np.zeros(self.numInFeatures)

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
        if self.tokens.size < self.numInFeatures:
            self.padWithZeros()

        if self.tokens.size > self.numInFeatures:
            self.tokens = self.tokens[0:self.numInFeatures]
            self.attentionMask = self.attentionMask[0:self.numInFeatures]

    def padWithZeros(self):
        lenPadArray = self.numInFeatures - self.tokens.size
        padArray = np.zeros(lenPadArray, dtype=int)
        self.tokens = np.concatenate((self.tokens, padArray))
        self.attentionMask = np.concatenate((self.attentionMask, padArray))

    def concatenate(self, idsNp):
        if self.tokens.size > 0:
            self.tokens = np.concatenate((self.tokens, idsNp))
        else:
            self.tokens = idsNp
