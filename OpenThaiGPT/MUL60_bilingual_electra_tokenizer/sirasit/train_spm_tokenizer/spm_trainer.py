import json
import hydra
import datasets    
from datasets import Dataset
import json
import os
import sentencepiece as spm
from tqdm import tqdm
import transformers
from transformers import LlamaTokenizer


# const
PREPARE_DATASETS_KEY = "text_processed"
EOS_TOKEN = "</s>"
BOS_TOKEN = "<s>"
UNK_TOKEN = "<unk>"

BPE_MODE = "bpe"
UNIGRAM_MODE = "unigram"
CHAR_MODE = "char"
WORD_MODE = "word"


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


# prepare dataset function
def prepare_datasets(texts: dict) -> dict:
    prepared_texts = []
    for text in texts["text"]:
        prepared_texts.append(text)
    return {PREPARE_DATASETS_KEY: prepared_texts}

# dataset iterator
class DataSetColumnIterator:
    def __init__(self, dataset, column_name: str):
        self.dataset = iter(dataset)
        self.column_name = column_name

    def __iter__(self):
        for item in self.dataset:
            try:
                yield item[self.column_name]
            except KeyError:
                raise ValueError(f"Column '{self.column_name}' is not a valid index for the dataset")



def train_tokenizer(
    output_path: str,
    vocab_size: int,
    hf_dataset,
    vocab_file_name: str,
    model_file_name: str,
    mode: str = BPE_MODE
) :
    if not (mode == UNIGRAM_MODE or mode == BPE_MODE or mode == WORD_MODE or mode == CHAR_MODE):
        KeyError(f"mode mush be {UNIGRAM_MODE} or {BPE_MODE} or {WORD_MODE} or {CHAR_MODE}")
        
        
    # process dataset
    text_processed_dataset = hf_dataset.map(
        function=prepare_datasets,
        batched=True,
    )

    spm.SentencePieceTrainer.train(
    sentence_iterator=iter(
        DataSetColumnIterator(text_processed_dataset, PREPARE_DATASETS_KEY)
    ),
    model_prefix=output_path + "/" + vocab_file_name,
    vocab_size=vocab_size,
    model_type=mode,  # base on your requirement
    )

    print("SentencePiece tokenizer has been trained and saved to", output_path)

    # Load to LlamaTokenizer
    tokenizer = LlamaTokenizer(vocab_file=f"{output_path}/{model_file_name}")

    # special tokens
    tokenizer.eos_token = EOS_TOKEN
    tokenizer.bos_token = BOS_TOKEN
    tokenizer.unk_token = UNK_TOKEN

    # Save
    tokenizer.save_pretrained(output_path)

    print("LlamaTokenizer has been created and saved to", output_path)

