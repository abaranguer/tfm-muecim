import os

class FilesIndexCreator:
    def __init__(self):
        folderBase = 'data/datasets/EURLEX57K'
        folders = ['dev','test','train']
        
        for folder in folders:
            filesIndexFileName = f'{folderBase}/{folder}FilesIndex.txt'
            fd = open(filesIndexFileName, 'w')
            print(f'Iterating through folder {folder}')
            ix = 0
            fullNameFolder = f'{folderBase}/{folder}'
            for root, _, fullnames in os.walk(fullNameFolder):
                for name in fullnames:
                    fullName = f'{fullNameFolder}/{name}'
                    fd.write(f'{ix},{fullName}\n')
                    ix = ix + 1
                    if (ix % 1000) == 0:
                        print(f'Processing index {ix}')

            fd.close()

        print('Done!')

if __name__ == '__main__':
    FilesIndexCreator()

            

            
                  