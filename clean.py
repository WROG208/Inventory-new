#!/usr/bin/env python3

import csv

# Define the input and output CSV file paths
INPUT_CSV = "parts.csv"
OUTPUT_CSV = "parts_cleaned.csv"

# Define the required columns
REQUIRED_COLUMNS = [
    "Part Description", "Supplier", "Part # OEM", "Machine",
    "Location Shelf + Bin #", "Alternate part Number", "Alternate Manufacturer", "NOTES"
]

def clean_csv(input_file, output_file, required_columns):
    """
    Cleans the input CSV file by keeping only the required columns, removing empty rows,
    and stripping unnecessary double quotes from data.
    """
    try:
        # Read the input CSV file
        with open(input_file, 'r', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)

            # Check if all required columns exist in the input file
            input_columns = reader.fieldnames
            if not all(col in input_columns for col in required_columns):
                missing_columns = [col for col in required_columns if col not in input_columns]
                raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

            # Write the cleaned data to the output file
            with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
                writer = csv.DictWriter(outfile, fieldnames=required_columns)
                writer.writeheader()

                for row in reader:
                    # Check if the row is empty for the required columns
                    if any(row[col].strip() for col in required_columns):
                        # Remove quotes and keep only the required columns
                        cleaned_row = {
                            col: row[col].replace('"', '').strip() for col in required_columns
                        }
                        writer.writerow(cleaned_row)

        print(f"CSV cleaned successfully! Output written to {output_file}")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    clean_csv(INPUT_CSV, OUTPUT_CSV, REQUIRED_COLUMNS)
