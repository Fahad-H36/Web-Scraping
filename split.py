import pandas as pd
import os


def split_csv(file_name, n):
	
	# Read the original CSV file into a pandas DataFrame
	df = pd.read_csv(f'{file_name}.csv', encoding="ISO-8859-1")

	# Define the number of desired CSV files (n) and the number of rows per file (rows_per_file)
	rows_per_file = len(df) // n  # Number of rows per file

	# Create a directory to store the split CSV files
	os.makedirs('split_csvs', exist_ok=True)

	# Split the DataFrame and save each part as a separate CSV file
	for i in range(n):
		start_index = i * rows_per_file
		end_index = (i + 1) * rows_per_file
		if i == n - 1:  # For the last file, include any remaining rows
			end_index = len(df)
		split_df = df[start_index:end_index]
		output_filename = f'split_csvs/split_{start_index + 1}-{end_index}.csv'
		split_df.to_csv(output_filename, index=False)


file_name = input("Write the filename: ")
n = input("How many files do you want? ")

split_csv(file_name, int(n))