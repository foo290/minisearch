import os
import sys
import glob
import subprocess
import time
import shutil

# --- Configuration ---
INPUT_DIR = 'data'
TEMP_DIR = 'temp'
OUTPUT_DIR = 'output'
# Using relative paths for better portability
MAPPER_SCRIPT = os.path.join('minisearch', 'mapreduce', 'mapper.py')
REDUCER_SCRIPT = os.path.join('minisearch', 'mapreduce', 'reducer.py')
NUM_REDUCERS = 4


def cleanup():
    """Remove temporary and output directories if they exist."""
    print("Cleaning up previous run directories...")
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(TEMP_DIR)
    os.makedirs(OUTPUT_DIR)


def run():
    cleanup()
    start_time = time.time()

    # --- Phase 1: Map Phase ---
    print("--- Starting Map Phase ---")
    input_files = glob.glob(os.path.join(INPUT_DIR, '*.txt'))
    mapper_processes = []
    for i, filepath in enumerate(input_files):
        print(f"Starting mapper {i} for {os.path.basename(filepath)}...")
        # We pass TEMP_DIR as the 5th argument
        process = subprocess.Popen([
            'python', '-m', 'minisearch.mapreduce.mapper',
            filepath, str(i), str(NUM_REDUCERS), TEMP_DIR
        ])
        mapper_processes.append(process)

    # Wait for all mappers to complete
    for p in mapper_processes:
        p.wait()

    map_time = time.time()
    print(f"Map Phase completed in {map_time - start_time:.2f} seconds.")

    # --- Phase 2 & 3: Shuffle, Sort, and Reduce ---
    print("\n--- Starting Shuffle, Sort, & Reduce Phase ---")
    reducer_processes = []
    for i in range(NUM_REDUCERS):
        partition_files = glob.glob(os.path.join(TEMP_DIR, f'temp_mapper_*_part_{i}.out'))

        if not partition_files:
            print(f"No data for reducer {i}. Skipping.")
            continue

        print(f"Processing data for reducer {i}...")

        # 1. Shuffle & Combine
        reducer_input_path = os.path.join(TEMP_DIR, f'reducer_{i}_input.txt')
        with open(reducer_input_path, 'w', encoding='utf-8') as outfile:
            for fname in partition_files:
                with open(fname, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())

        # 2. Sort
        sorted_input_path = os.path.join(TEMP_DIR, f'reducer_{i}_sorted_input.txt')
        with open(reducer_input_path, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
        lines.sort()
        with open(sorted_input_path, 'w', encoding='utf-8') as outfile:
            outfile.writelines(lines)

        # 3. Reduce
        reducer_output_path = os.path.join(OUTPUT_DIR, f'part-r-{i:05d}')
        with open(sorted_input_path, 'r', encoding='utf-8') as stdin_file, \
                open(reducer_output_path, 'w', encoding='utf-8') as stdout_file:
            process = subprocess.Popen(
                ['python', '-m', 'minisearch.mapreduce.reducer'],  # Changed how we call the module
                stdin=stdin_file, stdout=stdout_file
            )
            reducer_processes.append(process)

    # Wait for all reducers to complete
    for p in reducer_processes:
        p.wait()

    reduce_time = time.time()
    print(f"Reduce Phase completed in {reduce_time - map_time:.2f} seconds.")

    # --- Phase 4: Final Aggregation ---
    print("\n--- Aggregating Final Output ---")
    final_output_path = os.path.join(OUTPUT_DIR, 'inverted_index.txt')
    with open(final_output_path, 'w', encoding='utf-8') as outfile:
        # Important: only look for files that were actually created
        result_files = glob.glob(os.path.join(OUTPUT_DIR, 'part-r-*'))
        for fname in sorted(result_files):
            with open(fname, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())

    end_time = time.time()
    print(f"\nSuccessfully created final index at '{final_output_path}'.")
    print(f"Total execution time: {end_time - start_time:.2f} seconds.")


if __name__ == '__main__':
    run()