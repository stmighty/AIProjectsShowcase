import os
import json
import hydra
from datasets import load_dataset, Dataset

def load_jsonl_files(directory, num_files="all"):
    texts = []
    if(num_files == "all") :
        for filename in sorted(os.listdir(directory)):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    data = json.loads(line)
                    texts.append(data["text"])
    
    else :
        file_count = 0
        for filename in sorted(os.listdir(directory)):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    data = json.loads(line)
                    texts.append(data["text"])
            file_count += 1
            if file_count >= num_files:
                break
            
    return texts



@hydra.main(version_base=None, config_path="./configfolder", config_name="config")
def main(cfg) :
    directory_path = cfg.visualize_directory_path

    # load texts ffile
    texts = load_jsonl_files(directory_path, num_files=20)

    # create a Hugging Face dataset
    hf_dataset = Dataset.from_dict({"text": texts})

    print("Dataset created with", len(hf_dataset), "texts")
    
if __name__ == "__main__":
    main()
