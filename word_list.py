class Word:
    """Class of single word, containing
        name - the word on english;
        translit - translation to russian,
        it also can be provided definition,
        and speach part attributes."""
        
    def __init__(self, name, translit):
        self.name = name
        self.translit = translit
        self.length = self.calc_word_lenght()
        self.spelling = self.check_spelling()
        self.definition = ''
        self.speach_part = ''

    def check_spelling(self):
        """Method to check spelling,
        if word doesn't contain ' ' it
        identified as correct."""        
        if self.name.find(' ') < 1:
            return 'correct'
        return 'wrong'
              
    def calc_word_lenght(self):
         return len(self.name) 


class OuterDictionary:
    """Class which provides tools for import of outer dictionary with following structure:
    english word; russian translation1, russian translation2, russian translation3 ..."""
    def __init__(self, file_path=None):
        self.word_dict = dict()
        if file_path is None:
            self.file_path = './words.txt'
        self.import_words()

    def import_words(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                try:
                    self.word_dict[line.split(';')[0]] = line.split(';')[1].strip()
                except IndexError as err:
                    print(f'Possibly string {i+1} of outer dictionary is corrupted "{line}"')


class WordsList:
    """Class which contains methods
    and interfaces to add words and their properties to te list"""
    def __init__(self):
        self.list_of_words =[]
        self.dict_of_words ={}
        
    def add_word(self, word):
        self.list_of_words.append(word)
        self.dict_of_words[word.name] = word

def main():
   word_list = WordsList()
   outer_dictionary = OuterDictionary()

   for k in outer_dictionary.word_dict.keys():
       word_list.add_word(Word(k, outer_dictionary.word_dict[k]))

   for key in word_list.dict_of_words.keys():
       print(f'{word_list.dict_of_words[key].name} - {word_list.dict_of_words[key].translit}')


if __name__ == '__main__':
    main()

