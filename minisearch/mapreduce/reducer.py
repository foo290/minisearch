import sys

current_word = None
current_docs = []

for line in sys.stdin:
    # The input from the sort command will be "word\tdoc_id"
    word, doc_id = line.strip().split('\t', 1)

    if current_word == word:
        current_docs.append(doc_id)
    else:
        if current_word:
            # A new word has started, so print the result for the previous word.
            # Use set() to get a unique list of documents.
            unique_docs = sorted(list(set(current_docs)))
            print(f'{current_word}\t{unique_docs}')

        current_word = word
        current_docs = [doc_id]

# Don't forget to print the last word!
if current_word == word:
    unique_docs = sorted(list(set(current_docs)))
    print(f'{current_word}\t{unique_docs}')