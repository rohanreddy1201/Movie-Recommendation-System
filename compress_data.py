import bz2
import shutil

# Paths to input and output files
input_file = "Datasets/cleaned_ratings_data.csv"
output_file = "Datasets/cleaned_ratings_data.csv.bz2"

# Compress the file
with open(input_file, "rb") as source:
    with bz2.BZ2File(output_file, "wb") as compressed:
        shutil.copyfileobj(source, compressed)

print(f"File compressed successfully to {output_file}")
