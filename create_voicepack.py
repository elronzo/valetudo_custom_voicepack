#!/usr/bin/env python3

import tarfile
import os
import http.server
import socketserver
import hashlib
import socket

PORT = 8000  # Define the port to serve on
COUNTRY_CODE = "US"  # Define the two-letter country code in uppercase
TAR_FILENAME = f"custom_voicepack_{COUNTRY_CODE}.tar.gz"  # Define the tar.gz filename

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory='.', **kwargs)  # Serve files from the current directory

def serve_tarfile():
    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("serving at port", PORT)
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped by user.")

def make_tarfile(output_filename, source_dir):
    try:
        with tarfile.open(output_filename, "w:gz") as tar:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    if file.endswith(".ogg"):  # Only add .ogg files to the tarball
                        tar.add(os.path.join(root, file), arcname=os.path.relpath(os.path.join(root, file), source_dir))
    except tarfile.TarError as e:
        print(f"Error creating tarfile: {e}")

def calculate_md5(filename):
    try:
        hasher = hashlib.md5()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except IOError as e:
        print(f"Error calculating MD5 checksum: {e}")

def get_ip_address():
    try:
        # Create a socket object
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Use a dummy IP and port to connect to
        s.connect(("8.8.8.8", 80))
        # Get the IP address of the network interface
        ip_address = s.getsockname()[0]
        # Close the socket
        s.close()
        return ip_address
    except Exception as e:
        print(f"Error retrieving IP address: {e}")
        return None

if __name__ == "__main__":
    if COUNTRY_CODE == "EN":
        print("Country code 'EN' is not allowed.")
    else:
        make_tarfile(TAR_FILENAME, ".")  # Tar.gz all .ogg files in the current directory
        md5sum = calculate_md5(TAR_FILENAME)
        if md5sum:
            print(f"Hash (MD5 checksum) of {TAR_FILENAME}: {md5sum}")

            # Get the IP address of the host
            ip_address = get_ip_address()
            if ip_address:
                url = f"http://{ip_address}:{PORT}/{TAR_FILENAME}"
                print(f"Serving file at: {url}")
                print(f"Language code: {COUNTRY_CODE}")
                serve_tarfile()  # Serve the tar.gz file
            else:
                print("Failed to retrieve IP address. Exiting.")
        else:
            print("Failed to calculate MD5 checksum. Exiting.")

