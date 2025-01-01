import torch
from tfm_EURLEX57KDataset import EURLEX57KDataset
from torch.utils.data import DataLoader, random_split


if __name__ == '__main__':
    print('Init')
    
    # ensures reproducibility
    torch.manual_seed(0)
    
    ds = EURLEX57KDataset('FilesIndex.txt')
    trainData, valData, testData = random_split(ds, [45000, 6000, 6000])

    trainDataLoader = DataLoader(trainData, batch_size=64, shuffle=True)
    valDataLoader = DataLoader(valData, batch_size=64, shuffle=True)
    testDataLoader = DataLoader(testData, batch_size=64, shuffle=True)

    # iterate through val batches
    for i, batch in enumerate(valDataLoader):
        print(f'Batch {i}: ')
        batchFileNames = batch.get('fileName')
        batchData = batch.get('data')
        batchLabels = batch.get('labels')

        for elem in zip(batchFileNames, batchData, batchLabels):
            print(f'fileName: {elem[0]}')
            print(f'data:\n{elem[1]}')
            print(f'labels:\n{elem[2]}')

            exit()
    print('Done!')
