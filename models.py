import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from prompts import BASE_PROMPT

"meta-llama/Llama-3.2-1B-Instruct"

class LLamaModel:

    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-1B-Instruct")
        self.model = AutoModelForCausalLM.from_pretrained(
            "meta-llama/Llama-3.2-1B-Instruct",
            torch_dtype=torch.bfloat16,
            low_cpu_mem_usage=True
            ).to('cuda')
        
    def prompt_formatter(self, query):
        base_prompt = BASE_PROMPT.format(query=query)

        dialog_prompt = [{"role": "user", "content": base_prompt}]

        inputs = self.tokenizer.apply_chat_template(
                    dialog_prompt,
                    tokenize=True,
                    add_generation_prompt=True,
                    return_tensors='pt',
                    return_dict=True
                ).to('cuda')
        return inputs
    
    def llm_output(self,query):
        inputs = self.prompt_formatter(query)

        output = self.model.generate(**inputs, do_sample=True, max_new_tokens=1024)
        decoded_outputs = self.tokenizer.batch_decode(output, skip_special_tokens=True)

        return decoded_outputs[0]

