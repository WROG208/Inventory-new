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
            print(f"Received POST data: {post_data}")

            # Parse the POST data
            data = urllib.parse.parse_qs(post_data)
            print(f"Parsed data: {data}")

            # Map form fields to the required columns
            new_part = {
                "Part Description": data.get("partdescription", [""])[0].strip(),
                "Supplier": data.get("supplier", [""])[0].strip(),
                "Part # OEM": data.get("partnumber", [""])[0].strip(),
                "Machine": data.get("machine", [""])[0].strip(),
                "Location Shelf and Bin": data.get("location", [""])[0].strip(),
                "Alternate part Number": data.get("alternatepartnumber", [""])[0].strip(),
                "Alternate Manufacturer": data.get("alternatemanufacturer", [""])[0].strip(),
                "NOTES": data.get("notes", [""])[0].strip(),
            }

            # Create a new row with all required columns
            new_row = [new_part.get(col, "") for col in REQUIRED_COLUMNS]
            print(f"Row to be added to CSV: {new_row}")

            # Append the new row to the CSV file
            with open(CSV_FILE, 'a', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
                writer.writerow(new_row)

            print("New part added successfully.")

            # Respond with a redirect and refresh meta tag
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"""
                <html>
                    <head>
                        <meta http-equiv="refresh" content="0;url=index.html">
                        <script>
                            window.location.href = 'index.html';
                        </script>
                    </head>
                    <body>
                        <p>Item added successfully. Redirecting...</p>
                    </body>
                </html>
            """)

        except Exception as e:
            print(f"Error processing POST request: {e}")
            self.send_error(500, "Internal Server Error", explain=str(e))


if __name__ == "__main__":
    port = 8000
    server_address = ('', port)
    print(f"Serving files from {BASE_DIR} on http://localhost:{port}/")

    try:
        httpd = HTTPServer(server_address, CustomHandler)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by user. Exiting gracefully...")
        httpd.server_close()  # Clean up resources
    except ConnectionAbortedError:
        print("Connection was aborted by the client.")
    except Exception as e:
        print(f"Unexpected error: {e}")
