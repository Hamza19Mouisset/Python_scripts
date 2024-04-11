import os
import hashlib
import time

def calculate_file_hash(filepath):
    """Calculate the SHA512 hash of a file."""
    with open(filepath, "rb") as f:
        file_hash = hashlib.sha512()
        for chunk in iter(lambda: f.read(4096), b""):
            file_hash.update(chunk)
    return file_hash.hexdigest()

def delete_baseline_if_already_exists():
    """Delete baseline.txt if it already exists."""
    if os.path.exists("./baseline.txt"):
        os.remove("./baseline.txt")

def create_baseline(folder):
    """Create baseline.txt with file paths and their corresponding hashes."""
    with open("./baseline.txt", "a") as baseline_file:
        for root, _, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = calculate_file_hash(file_path)
                baseline_file.write(f"{file_path}|{file_hash}\n")

def collect_new_baseline():
    """Collect new baseline by creating baseline.txt."""
    erase_baseline_if_already_exists()
    folder = "./Dir"
    create_baseline(folder)

def begin_monitoring():
    """Begin monitoring files with saved baseline."""
    file_hash_dictionary = {}

    if not os.path.exists("./baseline.txt"):
        folder = "./Dir"
        create_baseline(folder)

    with open("./baseline.txt", "r") as baseline_file:
        for line in baseline_file:
            file_path, file_hash = line.strip().split("|")
            file_hash_dictionary[file_path] = file_hash

    while True:
        time.sleep(1)

        for root, _, files in os.walk("./Dir"):
            for file in files:
                file_path = os.path.join(root, file)
                if not os.path.isfile(file_path):
                    continue

                current_hash = calculate_file_hash(file_path)

                if file_path not in file_hash_dictionary:
                    print(f"{file_path} has been created!")
                elif file_hash_dictionary[file_path] != current_hash:
                    print(f"{file_path} has changed!!!")
                else:
                    pass

        for file_path in list(file_hash_dictionary.keys()):
            if not os.path.exists(file_path):
                print(f"{file_path} has been deleted!")

if __name__ == "__main__":
    print("\nWhat would you like to do?\n")
    print("    A) Collect new Baseline?")
    print("    B) Begin monitoring files with saved Baseline?\n")
  
    response = input("Please enter 'A' or 'B': ").upper()
    
    if response == "A":
        collect_new_baseline()
    elif response == "B":
        begin_monitoring()
