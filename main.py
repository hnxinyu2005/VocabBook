from utils.check_files import check_and_fix_wordbooks
from utils.txt2csv import txt_to_csv

print("VocabBook")

print("检查初始单词本")
check_and_fix_wordbooks("default.csv")

print("检查初始单词本")
txt_file_path = "test_text.txt"
csv_filename = "default.csv"
txt_to_csv(txt_file_path, csv_filename)