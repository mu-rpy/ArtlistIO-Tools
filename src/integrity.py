import hashlib
import os
import json

def check_integrity(manifest_name):
    """Check the integrity of files against the existing MD5 manifest."""
    if not os.path.exists(manifest_name):
        print(f"[ERROR] Manifest {manifest_name} does not exist.")
        return

    with open(manifest_name, "r") as f:
        saved_hashes = f.readlines()

    for line in saved_hashes:
        expected_hash, file_path = line.split(maxsplit=1)
        file_path = file_path.strip()
        
        if os.path.exists(file_path):
            md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                while chunk := f.read(4096):
                    md5.update(chunk)
            current_hash = md5.hexdigest()

            if current_hash == expected_hash:
                print(f"[SUCCESS] {file_path} integrity verified.")
            else:
                print(f"[WARNING] {file_path} integrity check failed: "
                      f"expected {expected_hash}, found {current_hash}.")
        else:
            print(f"[WARNING] {file_path} does not exist.")

def get_platform():
    try:
        with open(os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "version.json")), 'r') as file:
            data = json.load(file)
            return data['platform']
    except FileNotFoundError:
        print("Error: The file 'data.json' was not found.")
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the file (invalid JSON format).")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    check_integrity(f"manifest.{get_platform()}.md5")