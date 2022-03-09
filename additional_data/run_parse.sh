python parse.py --raw_file s_english.txt --output_file diseases.txt --type en-ru --lower_case --sep ' - ' --rewrite --output_dir ./clean_data
python parse.py --raw_file homeenglish.txt --output_file diseases.txt --type ru-en --lower_case --output_dir ./clean_data
python parse_drugs.py --output_file drugs.txt --output_dir ./clean_data
python merge_data.py --files diseases.txt,drugs.txt --output_file merged_data.jsonl --output_dir ./clean_data