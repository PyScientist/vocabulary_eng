import random
import time


class Word:
    """Class of single word, containing
    :param name: The english word;
    :param translit: Translation to russian (Can be several meanings).
    It also can be provided definition, and speach part attributes after word instantiation"""
        
    def __init__(self, name, translit):
        self.name = name
        self.translation = translit
        self.length = self.calc_word_length()
        self.spelling = self.check_spelling()
        self.definition = ''
        self.speach_part = ''
        # Importance of the word could be between 0 and 10 where 10 is very important
        self.importance = 5

    def check_spelling(self):
        """Method to check spelling, if word doesn't contain ' ' it identified as correct."""
        if self.name.find(' ') < 1:
            return 'correct'
        return 'wrong'
              
    def calc_word_length(self):
        """Calculation of the word length"""
        return len(self.name)


class OuterDictionary:
    """Class which provides tools for import of outer dictionary with following structure:
    english word; russian translation1, russian translation2, russian translation3 ..."""
    def __init__(self, file_path=None):
        self.word_dict = dict()
        if file_path is None:
            self.file_path = './words.txt'
        else:
            self.file_path = file_path
        self.import_words()

    def import_words(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                try:
                    self.word_dict[line.split(';')[0]] = line.split(';')[1].strip()
                except IndexError as err:
                    # Conditions if line looks corrupted
                    if line.startswith('#'):
                        pass
                    else:
                        print(f'Possibly string {i+1} of outer dictionary is corrupted "{line}"')


class WordsList:
    """Class which contains methods
    and interfaces to add words and their properties to te list"""
    def __init__(self):
        self.dict_of_words = {}
        
    def add_word(self, word):
        "Add word from dict only word and set of its translations"
        self.dict_of_words[word.name] = word

    def get_words_from_external_dict(self, outer_dict):
        """Transfer words imported from text file (from prepared dict) to word list"""
        for k in outer_dict.word_dict.keys():
            self.add_word(Word(k, outer_dict.word_dict[k]))

    def choose_word_randomly(self):
        """Chose random word from WordList and print it"""

        random_word_obj = self.dict_of_words[list(self.dict_of_words.keys())[random.randint(0, len(self.dict_of_words)-1)]]
        print(random_word_obj.name)
        time.sleep(3.5)
        print(random_word_obj.translation)

    def print_all_words(self):
        """Print all words contained in WordList with their translations"""
        for key in self.dict_of_words.keys():
            print(f'{self.dict_of_words[key].name} - {self.dict_of_words[key].translation}')

    def check_the_word_presence(self, word):
        if word.strip().lower() in self.dict_of_words.keys():
            print(f'The word "{word}" with meanings "{self.dict_of_words[word].translation}" is in dictionary')
        else:
            print(f'The word "{word}" is not in the list would you like to add it?')


def main():
    word_list = WordsList()
    # Get words from outer dictionary
    word_list.get_words_from_external_dict(OuterDictionary('./words.txt'))
    # Work with word list
    word_list.choose_word_randomly()
    word_list.check_the_word_presence('accusing')

    # Need add exporting database in json object and back by serialization and deserialization
    # Add simple interface with Tkinter / Web interface (The hard way)?


if __name__ == '__main__':
    main()

