from transformers import pipeline

class BARTSummarizer:
    def __init__(self):
        print('BARTSummarizer')
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def summarize(self, mainBody):
        print(f'BARTSummarizer. mainBody:\n{mainBody}')

        summary = ''

        try:
            summary = self.summarizer(mainBody, max_length=130, min_length=30, do_sample=False)
        except Exception as err:
            summary = f"Error en generar el sumari:  {err=}, {type(err)=}"

        
        return f'{{"bart": {summary}}}'
