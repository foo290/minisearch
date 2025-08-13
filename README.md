# Scalable Search Indexer: A MapReduce Simulation in Python

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

This project is a high-fidelity simulation of a distributed MapReduce system, implemented entirely in Python. It processes a large collection of text documents to build a foundational data structure of search engines: an **inverted index**.

The primary goal is not just to produce the correct output, but to accurately model the real-world architecture of a distributed framework like Apache Hadoop. This includes simulating parallel worker processes, decentralized partitioning, a disk-based shuffle and sort phase, and final aggregation.

## Project Overview

The system takes a directory of text documents as input and produces a single `inverted_index.txt` file as output. This index maps each unique word (token) to a list of all documents in which it appears, enabling extremely fast keyword-based lookups.

The workflow is orchestrated by a master script (`main.py`) that manages and coordinates the distinct phases of a MapReduce job, demonstrating a deep understanding of distributed data processing principles without requiring a full Hadoop cluster.

---

## Architectural Simulation

This project meticulously simulates the key phases of a MapReduce job:

1.  **Master Controller (`main.py`):** Acts as the job coordinator, initiating and monitoring all worker processes and managing the data pipeline.

2.  **Input Splitting:** The input data is pre-split into individual `.txt` files within the `data/` directory, with each file representing a data chunk for a Mapper.

3.  **Map Phase (Parallel & Decentralized):**
    *   `main.py` launches a separate `mapper.py` process for each input file, simulating parallel execution across a cluster.
    *   **Decentralized Partitioning:** Each `mapper.py` worker contains its own hash-based partitioner. It writes its key-value output directly to multiple temporary files on disk, one for each Reducer it targets (e.g., `temp_mapper_0_part_2.out`). This accurately models how a real Mapper spills its partitioned output to its local disk, eliminating central bottlenecks.

4.  **Shuffle & Sort Phase (The "Distributed Dance"):**
    *   **Shuffle:** The `main.py` orchestrator simulates the "pull" phase of the Reducers. For each conceptual Reducer, it groups all corresponding temporary partition files from disk (`*_part_0.out`, `*_part_1.out`, etc.).
    *   **Sort:** For each group of files, `main.py` first concatenates them and then performs an in-memory sort. This simulates a Reducer's crucial merge-sort step, which prepares a perfectly ordered input stream for the reduce logic.

5.  **Reduce Phase (Parallel Aggregation):**
    *   `main.py` launches a separate `reducer.py` process for each partition, feeding it the corresponding sorted data via `stdin`.
    *   Each Reducer aggregates the data for its assigned keys and writes its final output to a unique part-file (e.g., `part-r-00000`) in the `output/` directory.

6.  **Final Aggregation:** The master script concatenates all Reducer part-files into a single, comprehensive `inverted_index.txt` file.

---

## Key Features & Technologies

*   **Core Language:** Python 3
*   **Core Concepts:** MapReduce, Inverted Index, Distributed Systems Architecture, Data Pipelines, NLP.
*   **Process Management:** `subprocess` module to orchestrate parallel worker processes.
*   **File Management:** `os`, `glob`, `shutil` modules for managing the disk-based intermediate data flow.
*   **Text Processing:** A robust text normalization pipeline using **NLTK**, which includes:
    *   Lowercasing
    *   Tokenization and Punctuation Removal
    *   Stop Word Filtering
    *   **Lemmatization** to reduce words to their root form for higher-quality indexing.

---

## How to Run the Project

### Prerequisites

*   Python 3.8+
*   The NLTK library: `pip install nltk`
*   NLTK data modules. Run this in a Python shell to download them:
    ```python
    import nltk
    nltk.download('punkt')      # For tokenization
    nltk.download('stopwords')  # For stop words
    nltk.download('wordnet')    # For lemmatization
    ```

### Project Structure

Make sure your project is organized as follows for the imports to work correctly:
```
├── data/
│ ├── doc1.txt
│ └── doc2.txt
├── main.py
├── minisearch/
│ ├── init.py
│ └── mapreduce/
│  ├── init.py
│  ├── mapper.py
│  ├── reducer.py
│ └── process_text.py
└── README.md

```

### Execution

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/your-username/your-repository-name.git
    cd your-repository-name
    ```

2.  **Add Data:** Place your `.txt` document files inside the `data/` directory.

3.  **Run the Simulation:** Execute the main orchestrator script from the root directory.
    ```bash
    python main.py
    ```

The script will provide real-time feedback on each phase of the MapReduce job and clean up temporary directories. The final output will be located at `output/inverted_index.txt`.

---

## Sample Output

The output file `output/inverted_index.txt` will contain the final inverted index. Each line consists of a word, a tab character, and a Python list representation of the unique document IDs where that word was found.