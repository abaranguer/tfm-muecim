import torch
import torchtext

from tfm_EURLEX57KMainBodySimpleTokensGenerator import EURLEX57KMainBodySimpleTokensGenerator

class LabelLoader:
    def __init__(self):
        fp = open('data/datasets/EURLEX57K/EURLEX57K.json')
        self.labels = json.load(fp)
        print(f'Total d\'etiquetes: {len(self.labels)}')
        fp.close()

class VocabularyBuilder(self):
    def __init__():
        print('Building vocabulary...')
        tokensGenerator = EURLEX57KMainBodySimpleTokensGenerator()
        self.vocab = torchtext.vocab.build_vocab_from_iterator(tokensGenerator)
        print('Vocabulary builded.')
