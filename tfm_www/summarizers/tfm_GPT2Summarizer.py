from transformers import AutoModelForCausalLM, AutoTokenizer

class GPT2Summarizer:
    def __init__(self):
        print('GPT2Summarizer')
        self.model = AutoModelForCausalLM.from_pretrained('gpt2-medium')
        self.tokenizer = AutoTokenizer.from_pretrained('gpt2-medium')
        self.tokenizer.pad_token = self.tokenizer.eos_token

    def summarize(self, mainBody):
        mainBody += ' TL;DR: '
        print(f'GPT2Summarizer. mainBody:\n{mainBody}')

        try:
            input_ids = self.tokenizer(mainBody, return_tensors="pt").input_ids

            unknownTokenId = tokenizer.unk_token_id
            if unknownTokenId in input_ids:
                print(f'Trobat token desconegut {unknownTokenId} als input_ids. Es reemplaça amb "eos_token_id".')
                input_ids = torch.where(input_ids == unknownTokenId, self.tokenizer.eos_token_id, input_ids)

            summary = ''

            generatedTokens = model.generate(
                input_ids,
                do_sample = True,
                top_k = 50,
                top_p = 0.85,
                pad_token_id = self.tokenizer.eos_token_id,
                max_length = 100
            )
        
            promptAndSummary = ''

            for _, generatedOutput in enumerate(generatedTokens):
                promptAndSummary += self.tokenizer.decode(generatedOutput, skip_special_tokens = True)

            promptAndSummarySplitted =  promptAndSummary.split('TL;DR:')
            summary = promptAndSummarySplitted[1]

        except Exception as err:
            summary = f"Error en generar el sumari:  {err=}, {type(err)=}"
            
        return f'{{"gpt2": {summary}}}'
