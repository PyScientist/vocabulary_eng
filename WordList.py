import random
import time
from DbHandlers import DbTextAnalyser


class Word:
    """Class of single word, containing
    :param name: The english word;
    :param translations: Translation to russian (Can be several meanings).
    It also can be provided definition, speach part attributes after word instantiation
    importance and related topic. Initially the highest importance set is equal 5"""
        
    def __init__(self, name, speach_part='', translations='', definition='', importance=5, topic=''):
        self.name = name
        self.translations = translations
        self.definition = definition
        self.speach_part = speach_part
        # Importance of the word could be between 0 and 5 where 5 is very important
        self.importance = importance
        self.topic = topic
        self.length = self.calc_word_length()
        self.spelling = self.check_spelling()

    def check_spelling(self):
        """Method to check spelling, if word doesn't contain ' ' it identified as correct."""
        if self.name.find(' ') < 1:
            return 'correct'
        return 'wrong'
              
    def calc_word_length(self):
        """Calculation of the word length"""
        return len(self.name)


class OuterDictionary_txt:
    """Class which provides tools for import of outer dictionary with following structure:
    english word; russian translation1, russian translation2, russian translation3 ..."""
    def __init__(self, file_path=None, err_reporting=False):
        self.word_dict = dict()
        if file_path is None:
            self.file_path = './texts/vocabulary.txt'
        else:
            self.file_path = file_path
        self.import_words(err_reporting=err_reporting)

    def import_words(self, err_reporting=False):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                try:
                    self.word_dict[line.split(';')[0]] = line.split(';')[1].strip()
                except IndexError as err:
                    # Conditions if line looks corrupted
                    if line.startswith('~~~*~~~'):
                        pass
                    else:
                        if err_reporting:
                            print(f'Possibly string {i+1} of outer dictionary is corrupted "{line}"')


class WordsList:
    """Class which contains methods
    and interfaces to add words and their properties to te list"""
    def __init__(self):
        self.dict_of_words = dict()
        # Open connection to database
        self.db_text_analyser = DbTextAnalyser()
        
    def add_word(self, word):
        """Add word from dict only word and set of its translations"""
        self.dict_of_words[word.name] = word

    def get_words_from_external_dict(self, outer_dict):
        """Transfer words imported from text file (from prepared dict) to word list"""
        for name in outer_dict.word_dict.keys():
            self.add_word(Word(name=name, translations=outer_dict.word_dict[name]))

    def choose_word_randomly(self):
        """Chose random word from WordList and print it"""

        random_word_obj = self.dict_of_words[list(self.dict_of_words.keys())[random.randint(0, len(self.dict_of_words)-1)]]
        print(f'Please recall this word: {random_word_obj.name}')
        time.sleep(3.5)
        print(f'The word has following translation to Russian: {random_word_obj.translations}\n\n\n')

    def print_all_words(self):
        """Print all words contained in WordList with their translations"""
        for key in self.dict_of_words.keys():
            print(f'{self.dict_of_words[key].name} - {self.dict_of_words[key].translations}')

    def check_the_word_presence(self, word):
        if word.strip().lower() in self.dict_of_words.keys():
            print(f'The word "{word}" with meanings "{self.dict_of_words[word].translations}" is in dictionary')
        else:
            print(f'The word "{word}" is not in the list would you like to add it?')

    def load_words_from_dict_to_db(self):
        for key in self.dict_of_words.keys():
            self.db_text_analyser.add_record_words_t(self.dict_of_words[key].name,
                                                     self.dict_of_words[key].speach_part,
                                                     self.dict_of_words[key].translations,
                                                     self.dict_of_words[key].definition,
                                                     self.dict_of_words[key].importance,
                                                     self.dict_of_words[key].topic,
                                                     )

    def get_words_from_db(self):
        table_name = 'words'
        self.dict_of_words = dict()

        # Look how organised columns in db
        columns_names_num_dict = {}
        for i, name in enumerate(self.db_text_analyser.get_columns_names(table_name)):
            columns_names_num_dict[name] = i

        # Upload words into memory
        for word in self.db_text_analyser.get_records(table_name):
            self.add_word(Word(name=word[columns_names_num_dict['name']],
                               speach_part=word[columns_names_num_dict['speach_part']],
                               translations=word[columns_names_num_dict['translations']],
                               definition=word[columns_names_num_dict['definition']],
                               importance=word[columns_names_num_dict['importance']],
                               topic=word[columns_names_num_dict['topic']]))

def main():
    word_list = WordsList()
    # Get words from outer dictionary
    #word_list.get_words_from_external_dict(OuterDictionary_txt('./texts/vocabulary.txt', err_reporting=False))
    # Work with word list

    #word_list.load_words_from_dict_to_db()
    word_list.get_words_from_db()


    word_list.choose_word_randomly()
    #word_list.check_the_word_presence('accusing')

    # Need add exporting database in json object and back by serialization and deserialization
    # Add functionality to add word in dictionary, delete word from dictionary
    # Add simple interface with Tkinter / Web interface (The hard way)?

if __name__ == '__main__':
    main()

