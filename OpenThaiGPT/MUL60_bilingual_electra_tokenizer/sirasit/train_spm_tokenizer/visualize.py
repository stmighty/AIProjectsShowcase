import os
import json
from transformers import LlamaTokenizer

def read_jsonl(file_path, num_examples=3):
    texts = []
    #with open(file_path, 'r', encoding='utf-8') as file:
    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            texts.append(data["text"])
            if len(texts) >= num_examples:
                break
    return texts

# try reading jsonl file
file_paths = [
    "../preprocess_part/HF_V6_Colassal_deduplicated_128_09_decontaminated_128_03_blinded_json_preprocess/train/train_04.jsonl",
    "../preprocess_part/HF_V6_Colassal_deduplicated_128_09_decontaminated_128_03_blinded_json_preprocess/train/train_18.jsonl"
]
for path in file_paths:
    print(f"Examples from {path}:")
    for text in read_jsonl(path):
        print(text)
    print("\n")
    
    
    

# try using our tokenizer
# Load the LlamaTokenizer
tokenizer = LlamaTokenizer.from_pretrained('./spm_tokenizer2.model')

sample_text = 'ในนี้มืดจังเลยนะฮะ ตอนนี้ เรามาดูกันดีกว่าว่า นิทานพื้นบ้านไทยเรื่องไหน ที่มีคติสอนใจ ข้อคิดสอนใจ ที่น่าสนใจกันบ้าง เรื่องเหล่านี้ เหมาะกับเด็กที่กำลังโต คุณพ่อคุณแม่สามารถนำไปเล่าให้น้อง ๆ ฟังได้.'

# Tokenize using LlamaTokenizer from pretrained
encoded_text = tokenizer.encode(sample_text)
tokens = tokenizer.tokenize(sample_text)

print("Encoded Text:", encoded_text)
print("Tokens:", tokens)




# try using our tokenizer
# Load the LlamaTokenizer
tokenizer = LlamaTokenizer.from_pretrained('./model_output/spm_tokenizer2.model')

sample_text = 'ในนี้มืดจังเลยนะฮะ ตอนนี้ เรามาดูกันดีกว่าว่า นิทานพื้นบ้านไทยเรื่องไหน ที่มีคติสอนใจ ข้อคิดสอนใจ ที่น่าสนใจกันบ้าง เรื่องเหล่านี้ เหมาะกับเด็กที่กำลังโต คุณพ่อคุณแม่สามารถนำไปเล่าให้น้อง ๆ ฟังได้.'

# Tokenize using LlamaTokenizer from pretrained
encoded_text = tokenizer.encode(sample_text)
tokens = tokenizer.tokenize(sample_text)

print("Encoded Text:", encoded_text)
print("Tokens:", tokens)