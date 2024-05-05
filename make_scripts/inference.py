import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import pipeline

model_id = "/pure-mlo-scratch/trial-runs/meditron-7b/hf_checkpoints/instruct/sft/"

# load model and tokenizer
model = AutoModelForCausalLM.from_pretrained(model_id, use_cache=True, device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(model_id, use_cache=False)

# Set the prompt
prompt = "Hi, my head hurts and I feel dizzy noew, what should I do?"

# use a pipeline to generate text
pipe = pipeline("text-generation",
                model=model,
                tokenizer= tokenizer,    
                max_new_tokens = 2048,
                do_sample=True,
                top_k=10,
                num_return_sequences=1,
                eos_token_id=tokenizer.eos_token_id,
                return_full_text=False
                )

# generate from prompt
generated = pipe(prompt)
print(generated[0]['generated_text'])