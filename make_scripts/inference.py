import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import pipeline

model_id = "/pure-mlo-scratch/make_project/spring2024/trial-runs/meditron-7B-BHC/hf_checkpoint/"

# load model and tokenizer
model = AutoModelForCausalLM.from_pretrained(model_id, use_cache=True, device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(model_id, use_cache=False)

# Set the prompt
prompt = '''You are a medical assistant. Your task is to write the brief hospital course corresponding to the following hospital 
discharge.\n\nsex: \nF\n \nallergies: \naspirin\n \nchief complaint: \n\n\nmajor surgical or invasive procedure: \nintubation 
_\nbronchoscopy _ - no evidence of active bleed; observed clot\nbronchoscopy _ - minor active bleed in RUL; treated with \ncold 
saline and epi\n\nattach\n\nhistory of present illness: \n\n\npast medical history: \n\n\nphysical exam: \n\n\npertinent results: 
\nADMISSION LABS:\n\n\n_ 09:10AM BLOOD WBC-6.0 RBC-4.70 hgb-14.4 hct-45.5* \nMCV-97 MCH-30.6 MCHC-31.6* RDW-12.2 RDWSD-44.0 plt 
_\n_ 09:10AM BLOOD _\n_ 01:00PM BLOOD cTropnT-<0.01\n_ 08:50PM BLOOD calcium-8.3* phos-3.0 mg-1.6\n_ 01:16PM BLOOD _ pO2-54* 
pCO2-72* pH-7.21* \ncalTCO2-30 base XS-1\n_ 01:16PM BLOOD lactate-3.0*"'''

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