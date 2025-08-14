# Inverted Index SearchEngine using MapReduce in Python

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

This project is a custom, disk-based implementation of the MapReduce programming model, built from the ground up in Python. It processes a large collection of text documents to build a foundational data structure of search engines: an **inverted index**.

The system is designed as a functional, standalone framework that showcases the core mechanics of fault-tolerant, parallel data processing. The workflow is orchestrated by a master script (`main.py`) that manages the entire data pipeline, demonstrating the core principles of large-scale data processing on a single machine.

## Framework Architecture

The framework faithfully implements the key phases of a classic MapReduce job:

1.  **Master Controller (`main.py`):** Acts as the job coordinator, initiating and monitoring all worker processes and managing the data pipeline from start to finish.

2.  **Input Splitting:** The input data is pre-split into individual `.txt` files within the `data/` directory, with each file representing a data chunk for a Mapper task.

3.  **Map Phase (Parallel & Decentralized):**
    *   `main.py` leverages the `subprocess` module to launch `mapper.py` tasks in parallel, one for each input file.
    *   **Decentralized Partitioning:** Each `mapper.py` worker contains its own hash-based partitioner. It writes its key-value output directly to multiple temporary files on disk, one for each conceptual Reducer. This accurately mirrors how a distributed framework like Hadoop handles intermediate data, eliminating central bottlenecks.

4.  **Shuffle & Sort Phase (The "Distributed Dance"):**
    *   **Shuffle:** The `main.py` orchestrator performs the Shuffle phase. For each Reducer, it groups all corresponding temporary partition files from the Mappers (`*_part_0.out`, `*_part_1.out`, etc.).
    *   **Sort:** For each group of files, `main.py` first concatenates them and then performs an in-memory sort. This prepares a perfectly ordered input stream for each Reducer, mirroring the outcome of a distributed merge-sort.

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

```.
├── data/
│   ├── doc1.txt
│   └── doc2.txt
├── main.py
├── minisearch/
│   ├── __init__.py
│   └── mapreduce/
│       ├── __init__.py
│       ├── mapper.py
│       ├── reducer.py
│       └── process_text.py
└── README.md
```
### Execution
Clone the Repository:
```
git clone https://github.com/foo290/minisearch.git
cd minisearch
```

Add Data: Place your .txt document files inside the data/ directory.
Run the Framework: Execute the main orchestrator script from the root directory.

```
python main.py
```

The script will provide real-time feedback on each phase of the MapReduce job and clean up temporary directories. The final output will be located at output/inverted_index.txt.

### Sample Output
The output file output/inverted_index.txt will contain the final inverted index. Each line consists of a word, a tab character, and a Python list representation of the unique document IDs where that word was found.