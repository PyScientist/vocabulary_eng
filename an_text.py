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
       
       self.dicy = {'word':[], 'frequency':[], 'firstletter':[]}
       for key in self.uniq_words_dict.keys():
              self.dicy['word'].append(key)
              self.dicy['frequency'].append(self.uniq_words_dict[key])
              self.dicy['firstletter'].append(key[0])
              
       self.df_uniq = pd.DataFrame(self.dicy)     
       self.df_uniq.sort_values('firstletter', inplace=True)
              
   def print_stat(self):
        """Display important metrics"""
        print(self.n_words, self.n_uniq_words)
        pd.set_option('display.max_rows', 500)
        print(self.df_uniq)
        
        
def read_txt_file(file):
    with open(file, 'r') as f:
        text = f.read()
    return text


def main():
       file = './texts/Benefits and dangers of AI in Petropysics.txt'
       an_text1 = AnText()
       text = read_txt_file(file)
       an_text1.get_text(text)
       an_text1.print_stat()
       
       
if __name__ == '__main__':
       main()
       