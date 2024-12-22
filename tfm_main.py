import os
import json

import torch
import torchtext

import torchtext.vocab
import torchtext.transforms
from torchtext.data.utils import get_tokenizer
# from torchtext.data.functional import pad

# https://pytorch.org/text/stable/datasets.html#text-classification
# https://hussainwali.medium.com/transforming-your-text-data-with-pytorch-12ec1b1c9ae6
# conda install pytorch::torchtext

if __name__ == '__main__':
    fp = open('data/datasets/EURLEX57K/EURLEX57K.json')
    labels = json.load(fp)

    print(f'Total d\'etiquetes: {len(labels)}')
    fp.close()

    dev_folder = 'data/datasets/EURLEX57K/dev'
    for root, _, fullnames in os.walk(dev_folder):
        for name in fullnames:
            full_name = f'{dev_folder}/{name}'
            fp = open(full_name, 'r')
            json_file = json.load(fp)
            print('celex_id: ',json_file.get('celex_id'))
            print('header: ', json_file.get('header'))
            
            concepts = json_file.get('concepts')
            for concept in concepts:
                print('concept: ', labels.get(concept).get('label'),
                      labels.get(concept).get('alt_labels'))
            fp.close()
            break
        break

    tokenizer = get_tokenizer('basic_english')
    text = "This is a sentence."
    tokens = tokenizer(text)
    print(tokens)

    vocab = torchtext.vocab.build_vocab_from_iterator([tokens])
    ids = [vocab[token] for token in tokens]
    print(ids)

    # Load data
    reviews = ['This movie was great!', 'This movie was terrible.']
    tokenizer = torchtext.data.utils.get_tokenizer('basic_english')
    vocab = torchtext.vocab.build_vocab_from_iterator(
        tokenizer(review) for review in reviews
    )
    print('---------------------')
    # Apply transformations
    for review in reviews:
        print(review)
    print('---------------------')
    tokenized_reviews = [tokenizer(review) for review in reviews]
    for review in tokenized_reviews:
        print(review)
    print('---------------------')        
    numericalized_reviews = [[vocab[token] for token in review] for review in tokenized_reviews]
    for review in numericalized_reviews:
        print(torch.tensor(review))
    print('---------------------')
    # padded_reviews = [pad(review, (10,), pad_id=vocab['<pad>']) for review in numericalized_reviews]
    padder = torchtext.transforms.PadTransform(10, 0)
    padded_reviews = padder.forward(torch.tensor(numericalized_reviews))
    for review in padded_reviews:
        print(torch.tensor(review))

    # Use transformed data in model
    #model_input = torch.tensor(padded_reviews)
