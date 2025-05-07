# coding: utf-8
from flask import Flask, request
import json 
import pandas as pd
from classifiers.tfm_DistilBERTClassifier import DistilBERTClassifier
from classifiers.tfm_BERTClassifier import BERTClassifier
from classifiers.tfm_GPT2Classifier import GPT2Classifier

app = Flask(__name__)

@app.route('/<path:path>')
def static_file(path):
    if len(path)  == 0:
        path = 'index.html'
    return app.send_static_file(path)

@app.route('/getPage/<int:numPage>')
def getPage(numPage):
    if numPage < 1 or numPage > NUM_PAGES: 
        print('Número de pàgina no vàlid)')
        return '{"error":"Número de pàgina no vàlid"}';
    
    numPage -= 1
    limInf = numPage * ROWS_PER_PAGE
    limSup = min((numPage + 1) * ROWS_PER_PAGE, DF_LEN)

    dfReturn = df[limInf:limSup]
    json_data = dfReturn.to_json()
    
    return json_data

@app.route('/getJsonData', methods=['POST'])
def getJsonData():
    body = json.loads(request.data)
    jsonPath = body.get('jsonPath')
    return getJsonFile(jsonPath)
    
@app.route('/classifier/<int:idDataFrame>')
def getClassifications(idDataFrame):
    print('ID DataFrame rebut: ', idDataFrame)

    predDistilBert = distilBERTClassifier.predict(idDataFrame)
    predBert = bertClassifier.predict(idDataFrame)
    predGpt2 = gpt2Classifier.predict(idDataFrame)    

    fullResponse = f'{{"distilBert": {predDistilBert},"bert": {predBert}, "gpt2": {predGpt2}}}'
    
    return fullResponse

def getJsonFile(jsonPath):
    jsonFilePlain = None
    
    with open(f'./{jsonPath}','r') as fd:
        jsonFilePlain = fd.read()
        
    return jsonFilePlain
    
if __name__ == '__main__':
    df = pd.read_csv('csv/50LabelsDataFrame.csv')
    distilBERTClassifier = DistilBERTClassifier()
    bertClassifier = BERTClassifier()
    gpt2Classifier = GPT2Classifier()


    ROWS_PER_PAGE = 15
    DF_LEN = len(df)
    NUM_PAGES = int(DF_LEN / ROWS_PER_PAGE) + 1
    print('ROWS_PER_PAGE: ', ROWS_PER_PAGE)
    print('NUM_PAGES: ', NUM_PAGES)
    print('DF_LEN: ', DF_LEN)
    
    app.run(debug=True, port=5000)
