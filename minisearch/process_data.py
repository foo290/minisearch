from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize


def process_text(raw_text):
    # 1. Lowercase
    raw_text = raw_text.lower()

    # 2. Tokenize (and remove punctuation automatically)
    tokens = word_tokenize(raw_text)

    # 3. Remove Stop Words and non-alphabetic characters
    stop_words = set(stopwords.words('english'))
    clean_tokens = []
    for token in tokens:
        if token.isalpha() and token not in stop_words:
            clean_tokens.append(token)

    # 4. Lemmatize
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = []
    for token in clean_tokens:
        lemmatized_tokens.append(lemmatizer.lemmatize(token))

    return lemmatized_tokens


if __name__ == '__main__':
    with open('../data/doc1.txt', 'r', encoding='utf-8') as f:
        text = f.read()
        processed_words = process_text(text)
        print(processed_words)