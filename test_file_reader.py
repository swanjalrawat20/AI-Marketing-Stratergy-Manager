from app.tools.file_reader import read_file


print("=" * 40)
print("FILE READER TOOL TEST")
print("=" * 40)

print("\nStarting File Reader...")

result = read_file("sample_campaign.txt")

print("\n==============================")
print("FILE READER RESULT")
print("==============================")

print(result)

from app.tools.file_reader import read_file


print("=" * 40)
print("CSV FILE READER TEST")
print("=" * 40)

print("\nStarting File Reader...")

result = read_file("sample_campaign_data.csv")

print("\n==============================")
print("CSV FILE READER RESULT")
print("==============================")

print(result)