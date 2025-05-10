from transformers import pipeline

class BARTSummarizer:
    def __init__(self):
        print('BARTSummarizer')
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def summarize(self, mainBody):
        mainBody = mainBody[0]
        print(f'BARTSummarizer. mainBody:\n{mainBody}')

        summary = ''

        try:
            summary = self.summarizer(mainBody, max_length=130, min_length=30, do_sample=False)
        except Exception as err:
            summary = [{'summary_text': f"Error en generar el sumari:  {err=}, {type(err)=}"}]

        summaryText = summary[0].get('summary_text')

        return f'{{"bart": "{summaryText}"}}'
