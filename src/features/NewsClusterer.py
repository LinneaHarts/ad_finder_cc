from nltk.corpus import stopwords


def setup_nltk():
    stop_words = stopwords.words('english')
    stop_words.extend(['from', 'subject', 're', 'edu', 'use', 'not', 'would', 'say', 'could',
                           '_', 'be', 'know', 'good', 'go', 'get', 'do', 'done', 'try', 'many',
                           'some', 'nice', 'thank', 'think', 'see', 'rather', 'easy', 'easily',
                           'lot', 'lack', 'make', 'want', 'seem', 'run', 'need', 'even', 'right',
                           'line', 'even', 'also', 'may', 'take', 'come', 'hi', 'ha', 'wa', 'thi',
                           'to', 'one'])

   # warnings.filterwarnings("ignore", category=DeprecationWarning)
  #  logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.ERROR)
    return True


class NewsClusterer:

    def __init__(self):
        setup_nltk()
        print('News clusterer set up.')
