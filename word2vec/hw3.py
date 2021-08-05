import bz2
import gensim
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
data_file = 'news.crawl.bz2'

with bz2.open('news.crawl.bz2', 'rb') as f:
    for i, line in enumerate(f):
        print(line)
        break

def read_input(input_file):
    """This method reads the input file which is in gzip format"""
    
    logging.info("reading file {0}...this may take a while".format(input_file))
    
    with bz2.open (input_file, 'rb') as f:
        for i, line in enumerate (f): 

            if (i%10000==0):
                logging.info ("read {0} reviews".format (i))
            yield gensim.utils.simple_preprocess (line)

documents = list (read_input (data_file))
logging.info ("Done reading data file")

model = gensim.models.Word2Vec (documents, size=150, window=5, min_count=2, workers=8, iter=10)