1. Card description
Rationale:

We have to experiment about the best electra tokenizer

Step by step:

1.1 We have to sample 5% of dataset v6 tokenizer and save dataset to directory.
1.2 We have to sample engilsh data from pile dataset which make number of rows equal to Thai dataset.
1.3 Preprocess text data for training tokenizer following wangchanberta except text lowercase in both Thai and English data. https://github.com/vistec-AI/thai2transformers/blob/master/thai2transformers/preprocess.py
1.4 EDA preprocessed data (Just inspect text processor pipeline should return normal word and nothing weird).
1.5 Train Thai only and English only spm tokenizer with vocab size 15000 in each language.
1.6 Inspect vocab in spm vocab and you can discuss, retrain, and adjust tokenizer parameter with @peerawat.roj . Note: You can remove too long token in vocab.
1.7 Merge Thai and English spm tokenizer.

Definition of done:
    - Thai tokenizer
    - English tokenizer
    - Merged bilingual tokenizer




2. Structure of the project 

    2.1 MUL60_bilingual_electra_tokenizer/HF_V6_Colassal_deduplicated_128_09_decontaminated_128_03_blinded_json -> 
    here is the original data that we have

    2.2 MUL60_bilingual_electra_tokenizer/sirasit/preprocess_part -> 
    We need to EDA and preprocess and save the data from 1.1(HF_V6_Colassal_deduplicated_128_09_decontaminated_128_03_blinded_json) using MUL60_bilingual_electra_tokenizer/sirasit/preprocess_part/wangchanberta_preprocess.py except lowercase (https://github.com/vistec-AI/thai2transformers/blob/master/thai2transformers/preprocess.py) to MUL60_bilingual_electra_tokenizer/sirasit/preprocess_part/HF_V6_Colassal_deduplicated_128_09_decontaminated_128_03_blinded_json_preprocess

        2.2.1 MUL60_bilingual_electra_tokenizer/sirasit/preprocess_part/configfolder :
        Here is the config file before running the script you need to config 
            - random seed
            - sample fraction
            - input directory (of the original data)
            - output directory (of the preprocesded data)

        2.2.2 MUL60_bilingual_electra_tokenizer/sirasit/preprocess_part/preprocess.py :
        Here is the main file (script to run)

        2.2.3 MUL60_bilingual_electra_tokenizer/sirasit/preprocess_part/HF_V6_Colassal_deduplicated_128_09_decontaminated_128_03_blinded_json_preprocess :
        Here is the output folder after preprocessing (preprocessed data, we will use this folder to train tokenizer)

        2.2.4 MUL60_bilingual_electra_tokenizer/sirasit/preprocess_part/create_jsonl_folder.py :
        used in preprocess.py

        2.2.5 MUL60_bilingual_electra_tokenizer/sirasit/preprocess_part/wangchanberta_preprocess.py :
        used in preprocess.py

        2.2.6 MUL60_bilingual_electra_tokenizer/sirasit/preprocess_part/visualize.py :
        Here is just visualize file

        2.2.7 MUL60_bilingual_electra_tokenizer/sirasit/preprocess_part/outputs/2024-01-13 :
        not sure what is this folder

        2.2.8 MUL60_bilingual_electra_tokenizer/sirasit/preprocess_part/submit.sh :
        used only if you use cloud computing part (lanta), you can run by cd to the directory of this file and run sbatch submit.sh

    2.3 MUL60_bilingual_electra_tokenizer/sirasit/train_spm_tokenizer -> 
    after finish 1.2 (preprocess data) we have the new folder(which is preprocessed) (MUL60_bilingual_electra_tokenizer/sirasit/preprocess_part/HF_V6_Colassal_deduplicated_128_09_decontaminated_128_03_blinded_json_preprocess) we need to train the tokenizer following https://github.com/OpenThaiGPT/openthaigpt-pretraining/tree/main/src/model/scripts/spm_training. However this code has an error at --model_type (there is not spm model_type according to https://github.com/google/sentencepiece) so we use bpe instead.

        2.3.1 MUL60_bilingual_electra_tokenizer/sirasit/train_spm_tokenizer/configfolder :
        Here is the config file. Before running the script (train.py) you need to config
            - train_directory_path (preprocessed jsonl file)
            - output_path (output of the model)
            - vocab_size
            - vocab_file_name
            - model_file_name
            - train_mode (https://github.com/google/sentencepiece#train-sentencepiece-model)

        2.3.2 MUL60_bilingual_electra_tokenizer/sirasit/train_spm_tokenizer/train.py :
        this is the main part (script to run)

        2.3.3 MUL60_bilingual_electra_tokenizer/sirasit/train_spm_tokenizer/spm_trainer.py :
        used in train.py

        2.3.4 MUL60_bilingual_electra_tokenizer/sirasit/train_spm_tokenizer/model_output :
        this is the output of tokenizer model there are many vocab_size folder in here.

        2.3.5 MUL60_bilingual_electra_tokenizer/sirasit/train_spm_tokenizer/visualize.py :
        this is just visualize file.

        2.3.6 MUL60_bilingual_electra_tokenizer/sirasit/train_spm_tokenizer/submit.sh :
        used only if you use cloud computing part (lanta), you can run by cd to the directory of this file and run sbatch submit.sh
        



3. Which parts that you did it by yourself and which part by chatgpt
    * I wrote all config file and modified the structure to make it compatible with hydra.
    3.1 preprocess_part
        3.1.1 create_jsonl_folder -> chatgpt (it's rather complex to create jsonl file and that is not the main objective of this project)
        3.1.2 preprocess.py -> by myself 
        3.1.3 submit.sh -> by myself (example from https://openthaigpt.gitbook.io/openthaigpt-guideline/lanta/slurm)
        3.1.4 visualize.py -> by myself (except def load_jsonl_files)
        3.1.5 wangchanberta_preprocess -> base on code from github (change by myself) (from https://github.com/vistec-AI/thai2transformers/blob/master/thai2transformers/preprocess.py) and just remove .tolower()
        3.1.6 config.yaml -> by myself
    3.2 train_spm_tokenizer
        3.2.1 spm_trainer -> base on example (change by myself) (base on https://github.com/OpenThaiGPT/openthaigpt-pretraining/blob/main/src/model/openthaigpt_pretraining_model/tokenizers/spm_trainer.py) except def load_jsonl_files(chatgpt)
        3.2.2 train.py -> by myself
        3.2.3 visualize.py -> by myself + by chatgpt
        3.2.4 config.yaml -> by myself
        3.2.5 submit.sh -> by myself (example from https://openthaigpt.gitbook.io/openthaigpt-guideline/lanta/slurm)
        3.2.6 model_output -> here is output folder of the model not "outputs" folder 


4. Problems during this card and how you solve them
    4.1 preprocess tokenizer have some mistake but you are in the process of training tokenizer


5. What did you learn from this project 
    5.1 You learnt about hydra (using config file) (no hardcoding anymore)
        5.1.1 using hydra 
        5.1.2 ./ refer to the current directory 
        5.1.3 ../ refer to the above directory ex. in MUL60_bilingual_electra_tokenizer/sirasit/preprocess_part/configfolder/config.yaml and MUL60_bilingual_electra_tokenizer/sirasit/preprocess_part/preprocess.py

        example 
        However, when running via command line it if you run at sbatch exp/export.sh and in export.sh it run sth like python ../script/export.py
                                    the result is differ from   sbatch export.sh (you cd to exp) it depends on the path you run command not the file

        5.1.4 from ...(file) import ...(function from other file) you can see many example in this folder
        5.1.5 avoid running by run symbol, you should use command python ...(name of file) ex. python train.py instead (due to relative path error)
    5.2 You know more about using virtual machine
        5.2.1 what slurm file is -> output file (output of running)
        5.2.2 submit.sh -> how to run backend node (sbatch submit.sh), myqueue, sbalance, ...
        5.2.3 how to list env (conda env list), create , activate, deactivate, ... (https://openthaigpt.gitbook.io/openthaigpt-guideline/lanta/slurm)
        5.2.4 method of using lanta (https://openthaigpt.gitbook.io/openthaigpt-guideline/lanta/python-environments-in-slurm)
            - ml Miniconda3
            - conda env list and conda activate ... (your env) (or create new env)
            - Navigate to the directory containing the submit.sh file. Remember to specify your preferred file within submit.sh before running it 
            - run it by command sbatch submit.sh
            - you will get something like Submitted batch job 775043, you can use myqueue to see the detail
            - open the link for more information ex. kill the process, etc. 
            - you will get an error if you run sbatch submit.sh before activate your env
            
    5.3 fundamental of read/write text and json/jsonl file
           
    

6. Disclaimer 
    6.1 There are only 5 jsonl files in training data as an example. In the real VM, there are many thousands file, so the result you get from training on your local will be worse.
    6.2 Moreover, I will not add those files in git due to the size problem.
    6.3 If you have any questions, search on your local machine /Users/sirasittanrattanawong/Downloads/AIProjectsShowcase/OpenThaiGPT/MUL60_bilingual_electra_tokenizer

7. latest update 19/1/24 

