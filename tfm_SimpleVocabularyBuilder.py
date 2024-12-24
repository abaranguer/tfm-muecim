import torchtext.vocab

from tfm_EURLEX57KMainBodySimpleTokensGenerator import EURLEX57KMainBodySimpleTokensGenerator

class VocabularyBuilder:
    def __init__(self):
        print('Building vocabulary...')
        tokensGenerator = EURLEX57KMainBodySimpleTokensGenerator().generator()
        self.vocab = torchtext.vocab.build_vocab_from_iterator(tokensGenerator)
        print('Vocabulary builded.')
    
if __name__ == '__main__':
    print(f'Vocabulary length: {len(VocabularyBuilder().vocab)}')
