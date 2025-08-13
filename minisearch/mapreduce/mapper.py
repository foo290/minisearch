import sys
import os
import hashlib
from process_data import process_text  # Use relative import


def partitioner(key, num_reducers):
    """Simple hash-based partitioner."""
    key_bytes = key.encode('utf-8')
    hash_object = hashlib.md5(key_bytes)
    return int(hash_object.hexdigest(), 16) % num_reducers


def main():
    # We now expect 5 arguments
    if len(sys.argv) != 5:
        print("Usage: python mapper.py <input_filepath> <mapper_id> <num_reducers> <temp_dir>")
        sys.exit(1)

    input_filepath = sys.argv[1]
    mapper_id = int(sys.argv[2])
    num_reducers = int(sys.argv[3])
    temp_dir = sys.argv[4]  # The new argument

    partition_files = {}

    try:
        with open(input_filepath, 'r', encoding='utf-8') as f:
            text = f.read()
            words = process_text(text)

            for word in words:
                partition_index = partitioner(word, num_reducers)

                if partition_index not in partition_files:
                    # We now construct the path inside the provided temp directory
                    output_filename = f"temp_mapper_{mapper_id}_part_{partition_index}.out"
                    output_path = os.path.join(temp_dir, output_filename)
                    partition_files[partition_index] = open(output_path, 'a', encoding='utf-8')  # Use 'a' for append

                # Write to the correct partition file
                partition_files[partition_index].write(f'{word}\t{os.path.basename(input_filepath)}\n')

    finally:
        for fp in partition_files.values():
            fp.close()


if __name__ == '__main__':
    main()