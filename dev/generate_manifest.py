import hashlib
import os

def generate_manifest(suffix):
    manifest_name = f"manifest.{suffix}.md5"
    base_path = os.path.dirname(os.path.abspath(__file__))
    hashes = []
    
    files_to_hash = [
        os.path.normpath(os.path.join(base_path, "..", "src", "artlistio-vid.py")), 
        os.path.normpath(os.path.join(base_path, "..", "src", "artlistio-sfx.py")),
        os.path.normpath(os.path.join(base_path, "..", "src", "updater.py")),
        os.path.normpath(os.path.join(base_path, "..", "src", "integrity.py")),
        os.path.normpath(os.path.join(base_path, "..", "Pipfile.lock")),
        os.path.normpath(os.path.join(base_path, "..", "Pipfile")),
        os.path.normpath(os.path.join(base_path, "..", "start.bat")),
    ]
    
    for file_path in files_to_hash:
        if os.path.exists(file_path):
            md5 = hashlib.md5()
            with open(file_path, "rb") as f:
                while chunk := f.read(4096):
                    md5.update(chunk)
            hashes.append(f"{md5.hexdigest()} {file_path}")

    with open(manifest_name, "w") as f:
        f.write("\n".join(hashes))
    print(f"[SUCCESS] Created {manifest_name} in root directory.")

if __name__ == "__main__":
    generate_manifest(input("> "))
 