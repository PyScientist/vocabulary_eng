from collections import Counter
import pandas as pd


class TextAnalyser:
    """Analyser of text. Provides simple statistic of words usage.

    -With use of external vocabulary it is possible to identify which words you already know
    (they are in vocabulary), and which you better to learn (absent in vocabulary).
    External vocabulary can be set by function "add_external_vocabulary_words".
    Vocabulary words stored in attribute "vocabulary_words".

    -To use class the text need to be uploaded in the class attribute "text" with method "get_text"
    for which we need give file path to txt file.
    """

    def __init__(self):
        self.text_path = ''
        self.text = ''
        self.vocabulary_words = list()
        self.all_words = list()
        self.uniq_words = list()
        # Dictionary of words as keys and frequency of how often does word occur as values.
        self.uniq_words_dict = dict()
        self.number_of_uniq_words = 0
        self.df_unique_words = pd.DataFrame()
        self.df_unique_words_unknown = pd.DataFrame()
        self.df_unique_words_known = pd.DataFrame()

    @staticmethod
    def clear_word(word_to_clean: str) -> str:
        """Remove non-meaning symbols from given word, convert it to lowercase.
        :param word_to_clean: Word, which need to be cleaned.
        :return: clean word"""
        word_to_clean = word_to_clean.replace('\n', ' ')
        for symbol in ',.)(:;[]{}!?':
            word_to_clean = word_to_clean.replace(symbol, ' ')
        word_to_clean = word_to_clean.strip()
        if word_to_clean.startswith("‘"):
            word_to_clean = word_to_clean.replace("‘", '')
        if word_to_clean.endswith("’"):
            word_to_clean = word_to_clean.replace("’", '')
        return word_to_clean.lower()

    def get_text(self, text_path: str) -> None:
        """Read text from file by given path and upload text being red in attribute "text"
        After importing instantly analyse text with method "analyse_text". Additionally
        assign to attribute "text_path" path to currently imported text.
        :param text_path: Path to text
        """
        with open(text_path, 'r', encoding='utf-8') as f:
            self.text = f.read()
            self.text_path = text_path
            self.analyse_text()

    def analyse_text(self) -> None:
        """Prepare word lists of text inside "text" attribute and prepare statistics of it:
        1) Get clean list of all words as it encountered in text
        2) Prepare dataframe with uniq words sorted by their frequency;
        """
        self.all_words = [self.clear_word(w) for w in self.text.replace('\n', ' ').split(' ')]
        uniq_words_dict = Counter(self.all_words)
        # Prepare dataframe with uniq words sorted frequency order
        word_frequency_dict = {'word': [], 'frequency': [], 'first-letter': []}
        for key in uniq_words_dict.keys():
            if key!='':
                print(f"'{key}'")
                word_frequency_dict['word'].append(key)
                word_frequency_dict['frequency'].append(uniq_words_dict[key])
                word_frequency_dict['first-letter'].append(key[0])
            self.df_unique_words = pd.DataFrame(word_frequency_dict)
        self.df_unique_words.sort_values('frequency', inplace=True)
        self.df_unique_words.reset_index(drop=True, inplace=True)

        if self.vocabulary_words:
            self.df_unique_words_unknown = self.df_unique_words[~self.df_unique_words['word'].
                                            isin(self.vocabulary_words)]
            self.df_unique_words_known = self.df_unique_words[self.df_unique_words['word'].
                                          isin(self.vocabulary_words)]

    def add_external_vocabulary_words(self, external_vocabulary):
        """Load words from previously prepared vocabulary into object"""
        self.vocabulary_words = external_vocabulary.words

    def print_stat(self, uniq_words_print = True, known_words = False, unknown_words = False):
        """Display important metrics"""
        print(f'Total words amount: {len(self.all_words)} Uniq words amount: {self.df_unique_words.shape[0]}')
        pd.set_option('display.max_rows', 500)
        if uniq_words_print:
            print('Uniq words in the text:')
            print(self.df_unique_words[['word', 'frequency']])
        if known_words:
            print('Uniq words in the text which you know well:')
            print(self.df_unique_words_known[['word', 'frequency']])
        if unknown_words:
            print('Uniq words in the text which you dont know:')
            print(self.df_unique_words_unknown[['word', 'frequency']])


class ExternalVocabulary:
    """Class of external vocabulary
    :param vocabulary_file_path: Path to file where external vocabulary stored"""

    def __init__(self, vocabulary_file_path: str):
        self.file_path = vocabulary_file_path
        self.words = []
        self.read_vocabulary()

    def read_vocabulary(self):
        """Read data from vocabulary located by path provided in file_path and prepare list of strings
        where each string is word with its translation, string which start with ~ consider as comments"""
        with open(self.file_path, 'r', encoding='utf-8') as f:
            self.words = [string.split(';')[0] for string in f.read().split('\n') if string.startswith('~') is False]


def main():
    text_path = './texts/Senior Expert Data Science & Analytics OMV group vacancy.txt'
    text_analyser = TextAnalyser()
    external_vocabulary = ExternalVocabulary(vocabulary_file_path='texts/vocabulary.txt')
    text_analyser.add_external_vocabulary_words(external_vocabulary)
    text_analyser.get_text(text_path)
    text_analyser.print_stat()


if __name__ == '__main__':
    main()
