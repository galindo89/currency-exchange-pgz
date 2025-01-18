import os
import csv

def extract_file_names(folder_path, output_csv):
    """
    Extracts all file names from the specified folder and writes them to a CSV file.

    Args:
        folder_path (str): Path to the folder from which to extract file names.
        output_csv (str): Path to the output CSV file.
    """
    try:
        # Get the list of all files and directories
        file_list = os.listdir(folder_path)

        # Filter out only files (ignore directories)
        file_names = [file for file in file_list if os.path.isfile(os.path.join(folder_path, file))]

        # Write to CSV
        with open(output_csv, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["File Name"])
            for file_name in file_names:
                writer.writerow([file_name])

        print(f"File names successfully extracted to {output_csv}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
# Call the function with the desired folder path and output file name
extract_file_names("./readme-docs/testing/lighthouse", "output_file.csv")
