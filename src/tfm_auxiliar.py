
    # lines generator
    # linesGenerator = EURLEX57KMainBodyLinesGenerator()    
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
                num_part = 1
                for part in main_body:
                    num_part = num_part + 1
                    lines = part.split('\n')
                    num_lines = len(lines)
                    total_lines = total_lines + num_lines
                    lengths = [len(line) for line in lines]
                    line_max_len = max(lengths)
                    max_len = max(max_len, line_max_len)
                    total_length = sum(lengths)
                    for line in lines:
                        line_vector = tokenizer(line)




                        line_vector_length = len(line_vector)
                        max_line_vector_length = max(
                            max_line_vector_length,
                            line_vector_length)
                
                absolute_max_length = max(absolute_max_length, max_len)
                absolute_max_num_lines = max(absolute_max_num_lines, total_lines)
                absolute_max_line_vector_length = max(
                    absolute_max_line_vector_length,
                    max_line_vector_length)
            
                count = count + 1
                if count % 1000 == 0:
                    print('Count: ', count)

            print('absolute max  length: ', absolute_max_length)
            print('absolute_max_num_lines: ', absolute_max_num_lines)
            print('absolute_max_lines_vector_length: ',
                absolute_max_line_vector_length)
            print('---------------------')
        

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
