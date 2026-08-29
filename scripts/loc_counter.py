import os
import sys

def count_lines(directory):
    total_lines = 0
    file_counts = {}
    for root, dirs, files in os.walk(directory):
        if '.git' in dirs:
            dirs.remove('.git')
        if '__pycache__' in dirs:
            dirs.remove('__pycache__')
        for file in files:
            if file.endswith('.py') or file.endswith('.md') or file.endswith('.json') or file.endswith('.txt'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = len(f.readlines())
                        total_lines += lines
                        file_counts[filepath] = lines
                except Exception as e:
                    pass
    return total_lines, file_counts

if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    total, breakdown = count_lines(root_dir)
    print("=" * 60)
    print(f"RESEARCH PROTOTYPES PLATFORM - TOTAL LOC COUNTER")
    print("=" * 60)
    print(f"Total Files Analyzed: {len(breakdown)}")
    print(f"Total Lines of Code (LOC): {total:,}")
    print("=" * 60)
    if total >= 50000:
        print(" SUCCESS: Codebase exceeds 50,000 LOC requirement!")
    else:
        print(f" WARNING: Codebase currently at {total} LOC (< 50,000).")
