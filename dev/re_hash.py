import subprocess
import os

def update_version_and_push():
    commit_msg = input("commit name: ")
    version_path = os.path.join("src", "version")

    subprocess.run(["git", "add", "."], check=True)

    # 1. Get the hash that WILL be created
    # 'write-tree' + 'commit-tree' predicts the hash of the next commit
    tree_hash = subprocess.check_output(["git", "write-tree"]).decode().strip()
    parent_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()
    
    # This predicts the hash based on the current state
    final_hash = subprocess.check_output([
        "git", "commit-tree", tree_hash, "-p", parent_hash, "-m", commit_msg
    ]).decode().strip()

    # 2. Update the file with that predicted hash
    with open(version_path, "r") as f:
        lines = f.readlines()
    
    while len(lines) < 3:
        lines.append("\n")
    
    lines[2] = final_hash + "\n"
    
    with open(version_path, "w") as f:
        f.writelines(lines)

    # 3. Finalize
    subprocess.run(["git", "add", version_path], check=True)
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)

if __name__ == "__main__":
    update_version_and_push()