python CreateFileIndices.py
echo "Dataset analyzer"
python tfm_DatasetAnalyzer.py
echo "50 labels dataset indices builder"
python tfm_50LabelsEURLEX57KBuilder.py
echo "50 labels dataframe builder"
python tfm_50KabelsEURLEX57KDataFrameBuilder.py
echo "Done!"
