import os
import json

import torch
import torchtext

#import torchtext.vocab
#import torchtext.transforms

#tokenizer
from torchtext.data.utils import get_tokenizer
# alternative: import spacy   

# Data loader
#from torch.utils.data import DataLoader, Dataset

# from torchtext.data.functional import pad

# https://pytorch.org/text/stable/datasets.html#text-classification
# https://hussainwali.medium.com/transforming-your-text-data-with-pytorch-12ec1b1c9ae6
# conda install pytorch::torchtext

# https://www.datacamp.com/tutorial/nlp-with-pytorch-a-comprehensive-guide

if __name__ == '__main__':
    # load labels
    fp = open('data/datasets/EURLEX57K/EURLEX57K.json')
    labels = json.load(fp)
    print(f'Total d\'etiquetes: {len(labels)}')
    fp.close()
    print('---------------------')

    # tokenizer
    tokenizer = get_tokenizer('basic_english')

    # iterate through dev set
    count = 0

    absolute_max_length = 0
    absolute_max_num_lines = 0
    absolute_max_line_vector_length = 0
    folder_base = 'data/datasets/EURLEX57K/'
    folders = ['dev','test','train']
    for folder in folders:
        print('folder: ', folder)
        full_name_folder = f'{folder_base}{folder}'
        for root, _, fullnames in os.walk(full_name_folder):
            for name in fullnames:
                full_name = f'{full_name_folder}/{name}'
                fp = open(full_name, 'r')
                json_file = json.load(fp)
                main_body = json_file.get('main_body')
                total_length = 0
                total_lines = 0
                max_len = 0
                max_line_vector_length = 0
                count = 0
                # print('cedex_id: ', json_file.get('celex_id'))
                # print('num_parts of main_body: ', len(main_body))

                num_part = 1
                for part in main_body:
                    # print('num_part: ', num_part)
                    num_part = num_part + 1
                    lines = part.split('\n')
                    num_lines = len(lines)
                    total_lines = total_lines + num_lines
                    # print('num_lines: ', num_lines)
                    lengths = [len(line) for line in lines]
                    line_max_len = max(lengths)
                    # print('line max_length: ', line_max_len)
                    max_len = max(max_len, line_max_len)
                    total_length = sum(lengths)
                    for line in lines:
                        line_vector = tokenizer(line)
                        line_vector_length = len(line_vector)
                        max_line_vector_length = max(
                            max_line_vector_length,
                            line_vector_length)

                # print('total length: ', total_length)
                # print('total lines: ', total_lines)
                # print('line max_len: ', max_len)
                # print('max_line_vector_length: ', max_line_vector_length)
                
                absolute_max_length = max(absolute_max_length, max_len)
                absolute_max_num_lines = max(absolute_max_num_lines, total_lines)
                absolute_max_line_vector_length = max(
                    absolute_max_line_vector_length,
                    max_line_vector_length)
            
                #concepts = json_file.get('concepts')
                #for concept in concepts:
                #    print('concept: ', labels.get(concept).get('label'),
                #          labels.get(concept).get('alt_labels'))
                #fp.close()

                count = count + 1
                if count % 1000 == 0:
                    print('Count: ', count)
                
                    # print('---------------------')

            print('absolute max  length: ', absolute_max_length)
            print('absolute_max_num_lines: ', absolute_max_num_lines)
            print(
                'absolute_max_lines_vector_length: ',
                absolute_max_line_vector_length)
            print('---------------------')
        
            '''
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
            padder = torchtext.transforms.PadTransform(10, 0)
            padded_reviews = padder.forward(torch.tensor(numericalized_reviews))
            for review in padded_reviews:
                print(torch.tensor(review))

            # Use transformed data in model
            #model_input = torch.tensor(padded_reviews)
            '''
