#!/usr/bin/env python3

import os
import shutil
import subprocess
import webbrowser
import time
import sys

# Define constants
INSTALL_DIR = r"C:\Inventory"
FILES_TO_COPY = ["add_to_csv.py", "500.html", "index.html", "add_item.html", "inventory.ico", "404.html", "dribbble_1.gif", "parts.csv", "Favicon.ico"]
SERVER_SCRIPT = "add_to_csv.py"
HTML_PAGE = "http://localhost:8000/index.html"
LOG_FILE = os.path.join(INSTALL_DIR, "error_log.txt")

def get_resource_path(relative_path):
    """
    Get the absolute path to a resource. Works for dev and PyInstaller bundle.
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def log_error(message):
    """
    Logs errors to a file.
    """
    with open(LOG_FILE, "a") as log:
        log.write(f"{time.ctime()} - {message}\n")

def setup_inventory_folder():
    """
    Ensures the required folder and files exist in the target directory.
    """
    try:
        if not os.path.exists(INSTALL_DIR):
            print(f"Creating directory: {INSTALL_DIR}")
            os.makedirs(INSTALL_DIR)

        # Copy all required files
        for file in FILES_TO_COPY:
            src = get_resource_path(file)
            dest = os.path.join(INSTALL_DIR, file)
            if not os.path.exists(dest):
                print(f"Copying {file} to {INSTALL_DIR}")
                shutil.copy(src, dest)

    except Exception as e:
        log_error(f"Error setting up inventory folder: {e}")
        raise


def start_server():
    """
    Starts the Python server in the background.
    """
    try:
        server_script_path = os.path.join(INSTALL_DIR, SERVER_SCRIPT)
        if not os.path.exists(server_script_path):
            raise FileNotFoundError(f"Server script '{server_script_path}' not found.")

        subprocess.Popen(
            ["pythonw", server_script_path],
            cwd=INSTALL_DIR,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"Server started with '{SERVER_SCRIPT}'.")
    except Exception as e:
        log_error(f"Error starting server: {e}")
        raise

def open_browser():
    """
    Opens the default web browser to the index.html page.
    """
    try:
        time.sleep(2)  # Give the server time to start
        webbrowser.open(HTML_PAGE)
        print(f"Browser opened to {HTML_PAGE}.")
    except Exception as e:
        log_error(f"Error opening browser: {e}")
        raise

if __name__ == "__main__":
    try:
        print("Setting up inventory system...")
        setup_inventory_folder()
        start_server()
        open_browser()
        print("System is running. You can now use the browser to search or add parts.")
    except Exception as e:
        log_error(f"Fatal error: {e}")
        print(f"An error occurred. Check {LOG_FILE} for details.")
    finally:
        input("Press Enter to close...")
