import hydra
from create_jsonl_folder import load_process_save_jsonl_files


@hydra.main(version_base=None, config_path="./configfolder", config_name="config")
def main(cfg) :
    # Set the input and output directory paths
    input_directory_path = cfg.input_directory_path
    output_directory_path = cfg.output_directory_path

    # Process the files
    load_process_save_jsonl_files(input_directory_path, output_directory_path, sample_fraction=cfg.sample_fraction, seed=cfg.seed)

    print("JSONL files have been processed and saved.")
    
if __name__ == "__main__":
    main()
    





