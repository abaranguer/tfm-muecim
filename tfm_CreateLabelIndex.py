import numpy as np
import json
from tfm_LabelLoader import LabelLoader

class LabelIndexCreator:
    def __init__(self):
        ll = LabelLoader()
        labelKeys = ll.labels.keys()
        i = 0
        self.indexLabels = {}
        fd = open('LabelIndex.txt','w')

        for labelKey in labelKeys:
            self.indexLabels[labelKey] = i
            fd.write(f"{i},'{labelKey}'\n")
            i = i + 1
            
        fd.close()

if __name__ == '__main__':
    print('Init')
    labelIndex = LabelIndexCreator()
    print('Done!')
