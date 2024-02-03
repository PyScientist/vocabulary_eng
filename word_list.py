class Word:
    """Class of single word, containing
        name - the word on english;
        translit - translition to russian,
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

class WordsList():
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
   word_list.add_word(Word('bird', 'птица'))
   word_list.add_word(Word('anxiety', 'тревожность'))
   word_list.add_word(Word('internalize', 'усвоить'))
   dict_new_words = {'subconsciously': 'подсознательно',
                                      'vet': 'проверять',
                                      'consistent': 'последовательный, стабильный, постоянный, постоянный',
                                      'overcome': 'преодолеть'}

   for k in dict_new_words.keys():
       word_list.add_word(Word(k, dict_new_words[k]))

   for key in word_list.dict_of_words.keys():
       print(f'{word_list.dict_of_words[key].name} - {word_list.dict_of_words[key].translit}')

