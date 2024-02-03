
class AnText:
   
   def __init__(self):
       self.text = ''
       self.n_words = 0
       self.all_words = []
       
   def get_text(self, text):
       self.text = text
       self.get_length()
   
   def get_length(self):
       self.all_words = self.text.split(' ')
       self.uniq_words = list(set(self.all_words))
       self.n_words = len(self.all_words)
       self.n_uniq_words = 
       
       
   def print_stat(self):
        print(self.n_words, )
        print(self.all_words)
        
        


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
       