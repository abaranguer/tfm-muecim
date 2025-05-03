import os
import pandas as pd
import pickle

class GPT2DataFrameForTextGenBuilder:
	def __init__(self, baseDir='datatxt/datasets/EURLEX57K'):
		self.baseDir = baseDir
		self.eurlex57k = {}
	
	def buildDataFrame(self):	
		self.eurlex57k = {
		'train': self.buildFolderDataFrame(os.path.join(self.baseDir, 'train')),
		'dev': self.buildFolderDataFrame(os.path.join(self.baseDir, 'dev')),
		'test': self.buildFolderDataFrame(os.path.join(self.baseDir, 'test'))
		}

	def saveAll(self):
		self.saveDataFrame('train', '50LabelsGPT2DataFrameForTextGenTrain')
		self.saveDataFrame('dev', '50LabelsGPT2DataFrameForTextGenDev')
		self.saveDataFrame('test', '50LabelsGPT2DataFrameForTextGenTest')

		self.saveEurlex57k()

	def buildFolderDataFrame(self, folder):
		print(f'Processing folder: {folder}')
		data = []
		count = 0
		for fileName in os.listdir(folder):
                        fullPath = os.path.join(folder, fileName)
                        if os.path.isfile(fullPath):
                                with open(fullPath, 'r', encoding='utf-8') as fd:
                                        text = fd.read()
                                        data.append({'fileName': fileName, 'text': text})
                                count += 1
                                if count % 1000 == 0:
                                        print(f'Processing file num: {count}')

		return pd.DataFrame(data)

	def saveDataFrame(self, dataFrameName, dataFrameFileName):
		self.eurlex57k[dataFrameName].to_csv(f'{dataFrameFileName}.csv', index=False, encoding='utf-8')
		self.eurlex57k[dataFrameName].to_excel(f'{dataFrameFileName}.xlsx', index=False)

	def saveEurlex57k(self):
		pickleFileName = 'eurlex57k.pickle'
		with open(pickleFileName, 'wb') as fd:
		        pickle.dump(self.eurlex57k, fd)

	def loadDataFrameFromPickleFile(self):
		pickleFileName = 'eurlex57k.pickle'
		with open(pickleFileName, 'rb') as fd:
		        self.eurlex57k = pickle.load(fd)
