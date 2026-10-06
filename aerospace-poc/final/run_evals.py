import os
import subprocess

REAL = r'd:\aero\aerospace_structural_design_dataset.csv'
OUT_DIR = r'd:\aero\final\validation_reports'
SCRIPT = r'd:\aero\final\validate_dataset.py'

os.makedirs(OUT_DIR, exist_ok=True)

models_to_test = ['empirical_1000.csv', 'ctgan_1000.csv', 'tvae_1000.csv', 'tabudiff_1000.csv']

for m in models_to_test:
    syn_path = f'd:\\aero\\final\\per_model_datasets\\{m}'
    report_path = f'{OUT_DIR}\\{m.split(".")[0]}_report.md'
    if os.path.exists(syn_path):
        print(f'Running validation on {m}...')
        subprocess.run(['python', SCRIPT, REAL, syn_path, report_path, OUT_DIR])
    else:
        print(f'Missing: {syn_path}')
