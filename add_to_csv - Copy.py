#!/usr/bin/env python3

from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
import urllib.parse
import csv

# Set the base directory
BASE_DIR = r"C:\Inventory"
CSV_FILE = "parts.csv"  # Path to the CSV file
os.chdir(BASE_DIR)  # Change to the directory containing the files

# Define the required columns
REQUIRED_COLUMNS = [
    "Part Description", "Supplier", "Part # OEM", "Machine",
    "Location Shelf and Bin", "Alternate part Number", "Alternate Manufacturer", "NOTES"
]

class CustomHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        """
        Handle POST requests to append data to the CSV file.
        """
        try:
            print("Processing POST request...")

            # Read and decode the POST data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            print(f"Received POST data: {post_data}")  # Debugging: Raw POST data

            # Parse the POST data
            data = urllib.parse.parse_qs(post_data)
            print(f"Parsed data: {data}")  # Debugging: Parsed form data

            # Map form fields to the required columns
            new_part = {
                "Part Description": data.get("partdescription", [""])[0].strip(),
                "Supplier": data.get("supplier", [""])[0].strip(),
                "Part # OEM": data.get("partnumber", [""])[0].strip(),  # Correct mapping
                "Machine": data.get("machine", [""])[0].strip(),
                "Location Shelf an Bin": data.get("location", [""])[0].strip(),
                "Alternate part Number": data.get("alternatepartnumber", [""])[0].strip(),
                "Alternate Manufacturer": data.get("alternatemanufacturer", [""])[0].strip(),
                "NOTES": data.get("notes", [""])[0].strip(),
            }
            print(f"Mapped new part: {new_part}")  # Debugging: Mapped fields to columns

            # Create a new row with all required columns
            new_row = [new_part.get(col, "") for col in REQUIRED_COLUMNS]
            print(f"Row to be added to CSV: {new_row}")  # Debugging: Final row for CSV

            # Append the new row to the CSV file
            with open(CSV_FILE, 'a', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
                writer.writerow(new_row)
            print("New part added successfully.")  # Debugging: Confirmation of write

            # Redirect back to the form page
            self.send_response(302)
            self.send_header('Location', '/add_item.html')
            self.end_headers()
        except Exception as e:
            print(f"Error processing POST request: {e}")  # Debugging: Exception details
            # Send a custom 500 error
            self.send_error(500, "Internal Server Error", explain=str(e))

if __name__ == "__main__":
    port = 8000
    server_address = ('', port)
    print(f"Serving files from {BASE_DIR} on http://localhost:{port}/")
    httpd = HTTPServer(server_address, CustomHandler)
    httpd.serve_forever()

