import os
import glob

root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dirs = [
    'src/core/experimentation',
    'src/core/metrics',
    'src/core/lineage',
    'src/core/data',
    'src/domain/nlp',
    'src/domain/vision',
    'src/domain/tabular',
    'src/domain/reinforcement',
    'src/server',
    'src/ui',
    'tests',
    'scripts'
]

print(f"| {'Directory / Subsystem':<40} | {'File Count':<10} | {'Total LOC':<18} |")
print("|" + "-"*42 + "|" + "-"*12 + "|" + "-"*20 + "|")

grand_total = 0
total_files = 0
for d in dirs:
    full_d = os.path.join(root_dir, d)
    files = glob.glob(os.path.join(full_d, '*.py'))
    lines = 0
    for f in files:
        with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
            lines += len(fp.readlines())
    grand_total += lines
    total_files += len(files)
    print(f"| {d:<40} | {len(files):<10} | {lines:<18,} |")

# Add root files
root_files = ['README.md', 'requirements.txt', 'setup.py']
root_lines = 0
for rf in root_files:
    fp = os.path.join(root_dir, rf)
    if os.path.exists(fp):
        with open(fp, 'r', encoding='utf-8') as f:
            root_lines += len(f.readlines())
grand_total += root_lines
total_files += len(root_files)
print(f"| {'root configs (README, setup.py, etc.)':<40} | {len(root_files):<10} | {root_lines:<18,} |")

print("|" + "="*42 + "|" + "="*12 + "|" + "="*20 + "|")
print(f"| {'TOTAL CODE LINES':<40} | {total_files:<10} | {grand_total:<18,} |")
