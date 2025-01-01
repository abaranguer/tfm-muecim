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
    for batch in enumerate(valDataLoader):
        print(batched['data'].size(), batched['labels'].size())    

    print('Done!')
