from transformers import PegasusTokenizer, PegasusForConditionalGeneration

class PegasusXSUMSummarizer:
    def __init__(self):
        print('PegasusXSUMSummarizer')

        modelName = 'google/pegasus-xsum'
        self.tokenizer = PegasusTokenizer.from_pretrained(modelName)
        self.model = PegasusForConditionalGeneration.from_pretrained(modelName)

    def summarize(self, mainBody):
        print(f'PegasusXSUMSummarizer. mainBody:\n{mainBody}')


        summary = ''

        try:
            input_ids = self.tokenizer(mainBody, return_tensors='pt', truncation=True).input_ids

            output = self.model.generate(
                input_ids,
                max_length=100,
                num_beams=3,
                early_stopping=True
            )

            summary = self.tokenizer.decode(output[0], skip_special_tokens=True)
        except Exception as err:
            summary = f"Error en generar el sumari:  {err=}, {type(err)=}"

        return f'{{"pegasus": {summary}}}'
