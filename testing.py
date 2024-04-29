
#Step 2: Import necessary libraries
from transformers import AutoModelForSequenceClassification, AutoTokenizer, BitsAndBytesConfig, AutoModelForCausalLM, pipeline
import torch

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

#Step 3: Load the model
model_name = "manoj-dhakal/llama-3-8b-PhiloSloppy"
model_path = "/scratch/at5282/PhiloSloppy/llama-3-8b-PhiloSloppy"
tokenizer_path = "/scratch/at5282/PhiloSloppy/llama-3-8b-PhiloSloppy"
#model = AutoModelForCasual.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    model_path,
    use_safetensors = True,
    device_map="auto",
    quantization_config=bnb_config,
)


text_generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=128
)

def get_response(prompt):
  sequences = text_generator(prompt)
  gen_text = sequences[0]["generated_text"]
  return gen_text

prompt = "I am not very satisfied with my life today. I hate working."

llama3_response = get_response(prompt)

print(llama3_response)



