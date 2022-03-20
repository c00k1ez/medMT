# medMT
##  Huggingface pipeline
To reproduce:  
0. Create venv/conda env.
1. Download WMT2020 medical data:
```bash
python download_baseline_data.py
```
2. (not necessary) Parse additional data:
```bash
cd additional_data
pip install -r requirements.txt
bash run_parse.sh
cd ..
```
3. If you dont have `bc` util, install it. For example for linux you can do it via:  
```bash
apt install bc -y
```
4. Setup & run pipeline:
```bash
cd train_transformers
bash setup_env.sh
bash train.sh
```