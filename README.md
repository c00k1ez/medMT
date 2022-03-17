# medMT
##  Huggingface pipeline
To reproduce:  
0. Create venv/conda env.
1. Download WMT2020 medical data:
```bash
python download_baseline_data.py
```
2. Parse additional data:
```bash
cd additional_data
pip install -r requirements.txt
bash run_parse.sh
cd ..
```
3. Setup & run pipeline
```bash
cd train_transformers
bash setup_env.sh
bash train.sh
```