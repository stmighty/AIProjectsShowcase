import datasets    
from datasets import load_dataset, Dataset
from datetime import datetime
import datetime  # Import the datetime module
import random
import json
import os
from wangchanberta_preprocess import process_transformers


def process_entry(entry):
    # Apply the process_transformers function to the 'text' field
    entry["text"] = process_transformers(entry["text"])
    return entry

def save_jsonl_file(dataset, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        for entry in dataset:
            # Convert datetime objects to string
            for key, value in entry.items():
                if isinstance(value, datetime.datetime):
                    entry[key] = value.isoformat()

            json_line = json.dumps(entry, ensure_ascii=False)
            outfile.write(json_line + '\n')

def load_process_save_jsonl_files(input_directory, output_directory, sample_fraction=0.05, seed=42):
    # Set the random seed for reproducibility
    random.seed(seed)

    os.makedirs(output_directory, exist_ok=True)

    # List all files in the directory
    all_files = sorted(os.listdir(input_directory))
    
    # Calculate the number of files to sample
    num_files_to_sample = int(len(all_files) * sample_fraction)
    
    # Randomly sample files
    sampled_files = random.sample(all_files, num_files_to_sample)

    for filename in sampled_files:
        file_path = os.path.join(input_directory, filename)
        # Load the entire file as a dataset
        dataset = load_dataset('json', data_files=file_path, split='train', ignore_verifications=True, cache_dir=None)

        # Process the entire dataset
        processed_dataset = dataset.map(process_entry, load_from_cache_file=False)

        # Save the processed data back to JSONL
        output_file_path = os.path.join(output_directory, filename)
        save_jsonl_file(processed_dataset, output_file_path)



'''

def load_and_save_jsonl_files(input_directory, output_directory, num_files=2):
    os.makedirs(output_directory, exist_ok=True)
    file_count = 0
    
    for filename in sorted(os.listdir(input_directory)):
        print(file_count)
        if file_count >= num_files:
            break

        input_file_path = os.path.join(input_directory, filename)
        output_file_path = os.path.join(output_directory, filename)

        i = 0
        
        with open(input_file_path, 'r', encoding='utf-8') as infile, \
             open(output_file_path, 'w', encoding='utf-8') as outfile:
            for line in infile:
                i += 1
                if(i%100 == 0) :
                    print(i)
                entry = json.loads(line)
                # Process the text field using process_transformers
                entry["text"] = process_transformers(entry["text"])
                # entry["text"] = (entry["text"])
                json_line = json.dumps(entry, ensure_ascii=False)
                outfile.write(json_line + '\n')

        file_count += 1

# Set the input and output directory paths
input_directory_path = "/project/lt200067-mtfc/HF_V6_Colassal_deduplicated_128_09_decontaminated_128_03_blinded_json/train"
output_directory_path = "/project/lt200067-mtfc/sirasit/preprocess_part/HF_V6_Colassal_deduplicated_128_09_decontaminated_128_03_blinded_json_preprocess/train"

# Process the files
load_and_save_jsonl_files(input_directory_path, output_directory_path)

print("JSONL files have been processed and saved.")

'''