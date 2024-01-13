import datasets    
import hydra
from datasets import Dataset
from spm_trainer import load_jsonl_files
from spm_trainer import train_tokenizer


@hydra.main(version_base=None, config_path="./configfolder", config_name="config")
def main(cfg) :
    train_directory_path = cfg.train_directory_path

    # load texts file
    if cfg.jsonl_load_all:
        num_files = "all"
    else:
        num_files = cfg.jsonl_num_files
        
    texts = load_jsonl_files(train_directory_path, num_files)

    # create a Hugging Face dataset
    hf_dataset = Dataset.from_dict({"text": texts})

    print("Dataset created with", len(hf_dataset), "texts")
    output_path = cfg.output_path
    vocab_size = cfg.vocab_size  # you should change vocab_size

    train_tokenizer(output_path, vocab_size, hf_dataset, cfg.vocab_file_name, cfg.model_file_name, mode = cfg.train_mode)
    
    
if __name__ == "__main__":
    main()