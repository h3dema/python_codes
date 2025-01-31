import os
import re
from tqdm import tqdm


def rename_files_with_prefix(directory, *, prefix: str, new_prefix: str):
    """
    Renames files in a directory, changing prefixes from `prefix` to `new_prefix`.

    Args:
        directory: The path to the directory containing the files.
        prefix (str): The prefix that needs to be changed.
        new_prefix (str): The new value
    """

    try:
        files = [filename for filename in os.listdir(directory) if filename.startswith(prefix)]
      
        for filename in tqdm(files):
            new_filename = new_prefix + filename[len(prefix):]  # Create the new filename
            old_filepath = os.path.join(directory, filename)
            new_filepath = os.path.join(directory, new_filename)

            try:
                os.rename(old_filepath, new_filepath)
                # print(f"Renamed '{filename}' to '{new_filename}'")
            except OSError as e:
                print(f"Error renaming '{filename}': {e}")

    except FileNotFoundError:
        print(f"Directory '{directory}' not found.")
    except Exception as e:  # Catch other potential errors (e.g., permissions)
        print(f"An error occurred: {e}")



def rename_files_with_pattern(directory, old_pattern: str, new_pattern: str):
    """
    Renames files in a directory, replacing a pattern in the filename.

    Args:
        directory: The path to the directory.
        old_pattern (str): The regular expression pattern to search for.
        new_pattern (str): The replacement pattern (can include backreferences).
    """

    try:
        filenames = os.listdir(directory)  # Get the list of files *once*
        for filename in tqdm(filenames, desc="Renaming files"): # Use tqdm here
            match = re.search(old_pattern, filename)  # Use re.search for pattern matching

            # if no match just skip
            # TODO: move match out of the loop, i.e., filter filenames
            if match:
                new_filename = re.sub(old_pattern, new_pattern, filename) # Use re.sub for replacement
                if new_filename != filename: # Avoid renaming to same name
                    old_filepath = os.path.join(directory, filename)
                    new_filepath = os.path.join(directory, new_filename)
                    try:
                        os.rename(old_filepath, new_filepath)
                        # print(f"Renamed '{filename}' to '{new_filename}'")
                    except OSError as e:
                        print(f"Error renaming '{filename}': {e}")


    except FileNotFoundError:
        print(f"Directory '{directory}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")



if __name__ == '__main__':
    # Example with relative path (current directory)
    rename_files_with_prefix(".", prefix='p_', new_prefix='q_')

    # Example usage:
    directory_path = "."  # Replace with your directory
    old_pattern = r"p_(.*)"  # Example: Matches "p_" followed by anything (group 1)
    new_pattern = r"q_\1"  # Example: Replaces with "q_" + group 1

    rename_files_with_pattern(directory_path, old_pattern, new_pattern)

