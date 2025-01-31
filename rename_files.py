import os
from tqdm import tqdm


def rename_files(directory, *, prefix: str = "p_", new_prefix: str = "q_"):
    """
    Renames files in a directory, changing prefixes from "p_" to "q_".

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


if __name__ == '__main__':
    # Example with relative path (current directory)
    rename_files(".")
