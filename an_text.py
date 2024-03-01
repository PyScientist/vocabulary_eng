from collections import Counter
import pandas as pd

class AnText:
   """Represent analysed text object"""
   def __init__(self):
       self.text = ''
       self.n_words = 0
       self.n_uniq_words = 0
       self.all_words = []
       self.uniq_words = []
       self.woc_words = []
       self.dicy = {'word':[], 'frequency':[], 'firstletter':[]}
       self.df_uniq = pd.DataFrame(self.dicy)
       
   def get_text(self, text):
       """grabbing text and its prelim. analysis"""
       self.text = text
       self.get_words()
    
   def clear_word(self, wo):
       """remove nonmeaning symbols"""      
       wo = wo.strip()
       sy_list = ',.)(:;[]{}'
       for sy in sy_list:
          wo = wo.replace(sy, '')
       if wo.startswith("‘"):
           wo = wo.replace("‘", '')
       if wo.endswith("’"):
           wo = wo.replace("’", '')
       wo  = wo.lower()
       return wo
      
   def get_words(self):
       """Prepare word lists and count waord number"""
       self.all_words = self.text.split(' ')
       self.all_words = [self.clear_word(w) for w in self.all_words]
       self.uniq_words_dict = Counter(self.all_words)
       self.n_words = len(self.all_words)
       self.n_uniq_words = len(self.uniq_words_dict)
         
       # Prepare dataset with uniq words
       for key in self.uniq_words_dict.keys():
              self.dicy['word'].append(key)
              self.dicy['frequency'].append(self.uniq_words_dict[key])
              self.dicy['firstletter'].append(key[0])
       self.df_uniq = pd.DataFrame(self.dicy)
       self.dicy = {'word':[], 'frequency':[], 'firstletter':[]}
       self.df_uniq.sort_values('frequency', inplace=True)
              
   def print_stat(self):
        """Display important metrics"""
        print(self.n_words, self.n_uniq_words)
        pd.set_option('display.max_rows', 500)
        print(self.df_uniq)
    
   def add_woc_words(self, woc):
       """Load wards from previously prepared vocabulary"""
       self.woc_words = woc.words
       
   def remove_familiar(self):
       self.df_uniq = self.df_uniq[~self.df_uniq['word'].isin(self.woc_words)]
       self.n_uniq_words = self.df_uniq.shape[0]


class woc:
        def __init__(self, file):
            self.file = file
            self.words = []
            self.read_woc()
                    
        def read_woc(self):
           woc_text = read_txt_file(self.file)
           self.words = [word for word in woc_text.split('\n') if word.startswith('~')==False]
           
               
def read_txt_file(file):
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
    return text


def main():
       # txt_file = './texts/Benefits and dangers of AI in Petrophysics.txt'
       txt_file = './texts/ML derived correlation of Sw for complex lithology.txt'
       txt_file = './texts/ML derived porosity and permeability in Dakota group.txt'
       an_text1 = AnText()
       text = read_txt_file(txt_file)
       an_text1.get_text(text)
       woc_file = './texts/wocabulary.txt'
       woc1 = woc(woc_file)
       an_text1.add_woc_words(woc1)
       an_text1.remove_familiar()
       an_text1.print_stat()
       
if __name__ == '__main__':
       main()
       