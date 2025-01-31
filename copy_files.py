import os
import shutil
import hashlib
from tqdm import tqdm


def calculate_file_hash(filepath):
    """Calculates the SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    try:
        with open(filepath, "rb") as file:  # Open in binary mode
            while True:
                chunk = file.read(4096)  # Read in chunks
                if not chunk:
                    break
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e: #Handle file reading exceptions
        print(f"Error calculating hash for {filepath}: {e}")
        return None # Or handle it differently


def copy_files(src_dir, dest_dir, overwrite=False, hash_overwrite=False):
    """
    Copies files from a source directory (including subdirectories) to a 
    destination directory, with options for overwriting and hash checking.

    Args:
        src_dir: Path to the source directory.
        dest_dir: Path to the destination directory.
        overwrite: If True, overwrite existing files in the destination.
        hash_overwrite: If True, overwrite existing files with different hashes.
    """

    try:
        for root, _, files in tqdm(os.walk(src_dir), desc="Copying files"):  # Use os.walk for subdirectories
            for file in files:
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, src_dir)  # Get relative path
                dest_path = os.path.join(dest_dir, rel_path)

                os.makedirs(os.path.dirname(dest_path), exist_ok=True)  # Create dirs if necessary

                if os.path.exists(dest_path):
                    # destination file exists

                    if os.path.getmtime(src_path) > os.path.getmtime(dest_path): 
                        # Check modification time. Always overwrite if src is newer
                        shutil.copy2(src_path, dest_path)
                        # print(f"Older file replaced: {dest_path}")
                    
                    else:

                        if overwrite:
                            # overwrite is true, then copy !
                            shutil.copy2(src_path, dest_path)  # copy2 preserves metadata
                            # print(f"Overwrote: {dest_path}")

                        elif hash_overwrite:
                            # if hash_overwrite is true, source overwrites destination file.
                            # This option means that:
                            # - destination file is newer (or same date),
                            # but source file is different from destination
                            src_hash = calculate_file_hash(src_path)
                            dest_hash = calculate_file_hash(dest_path)
                            if src_hash != dest_hash:
                                shutil.copy2(src_path, dest_path)
                                # print(f"Hash Overwrote: {dest_path}")
                            #else: #Optional: Print when hashes are the same
                            #    print(f"Same Hash: {dest_path}")

                        # else:
                        #     print(f"Skipped (newer or same version): {dest_path}")

                else:
                    shutil.copy2(src_path, dest_path)
                    # print(f"Copied: {dest_path}")

    except FileNotFoundError:
        print(f"Source directory '{src_dir}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Example usage:
    src_directory = "src"  # Replace with your source directory
    dest_directory = "dst"  # Replace with your destination
    copy_files(src_directory, dest_directory, overwrite=False, hash_overwrite=True)