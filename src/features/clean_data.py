import nltk
import pandas as pd
import numpy as np

from src.features.ArchiveParser import ArchiveParser


def read_in_files(file_list, meta_folder, html_folder, output_file):
    """ Read in html and meta files, build dataframe and export to CSV
    """
    meta_path = meta_folder
    html_path = html_folder
    file_list = file_list
    ap = ArchiveParser(file_list=file_list, meta_path=meta_path, html_path=html_path)
    shows = ap.parse_file_list()
    shows.to_csv(output_file)
    print(shows.head())
    return shows


def make_sentences(input_file, output_file):
    df = pd.read_csv(input_file)
    show_sent = []

    for index, row in df.iterrows():
        sentences = nltk.sent_tokenize(str(row['snippet']))
        for s in sentences:
            sent = {'sentence': s, 'start_snip': row['start_snip'], 'end_snip': row['end_snip'],
                    'contributor': row['contributor'], 'runtime': row['runtime'], 'start_time': row['start_time'],
                    'stop_time': row['stop_time'], 'identifier': row['identifier'], 'subjects': row['subjects']}
            show_sent.append(sent)
        if index % 100 == 0:
            print('Just processed "{}"'.format(s))

    new_df = pd.DataFrame(show_sent)
    new_df.to_csv(output_file)
    return new_df


def clean_sentences(shows):
    shows[['sentence']] = shows['sentence'].str.replace('nan', '')
    shows[['sentence']] = shows['sentence'].str.replace('â™ª', '')
    shows[['sentence']] = shows['sentence'].str.replace('>>', '')
    shows[['sentence']] = shows['sentence'].str.replace('♪', '')
    shows = shows.dropna()
    shows = shows.reset_index()
    shows = shows.drop(columns=['index'])
    return shows


def combine_sentences(shows):
    sent_list = []
    shows = shows.dropna()
    for index, row in shows.iterrows():
        show_dict = dict(row)
        sent_list.append(show_dict)
        sentence = row['sentence']
        if len(sentence) > 0:
            if len(sentence.split()) < 4:
                if 0 < index < len(sent_list):
                    sent_list[index - 1]['sentence'] = sent_list[index - 1]['sentence'] + ' ' + sentence
                    sent_list[index]['sentence'] = ''
        if index % 1000 == 0:
            print('Just processed {} "{}"'.format(index, sentence))

    new_df = pd.DataFrame(sent_list)
    new_df['sentence'].replace('', np.nan, inplace=True)
    new_df.dropna(inplace=True)
    new_df.reset_index(inplace=True)
    new_df.drop(columns=['index'], inplace=True)
    new_df.head()
    return new_df


if __name__ == "__main__":
    #show_df = read_in_files(file_list='../../data/raw/search-fox-last-year.csv', meta_folder='../../data/raw/meta-foxnews',
     #                       html_folder='../../data/raw/html-foxnews',
     #                       output_file='../../data/interim/fox-last-year-parsed.csv')
     # show_df = make_sentences(input_file='../../data/interim/fox-last-year-parsed.csv',
     #                           output_file=r'../../data/interim/fox-last-year-sent.csv')

    #    show_df = make_sentences(input_file='../../data/interim/cnn-last-year-parsed.csv',
    #                             output_file=r'../../data/interim/cnn-last-year-sent.csv')

    show_df = pd.read_csv('../../data/interim/fox-last-year-sent.csv')
    show_df = clean_sentences(show_df)
    show_df.to_csv('../../data/interim/fox-last-year-sent-cleaned.csv')
# show_df = pd.read_csv('../../data/interim/cnn-last-year-sent-cleaned.csv')
# show_df = pd.read_csv('../../data/interim/short-cnn-test.csv')
    show_df = combine_sentences(show_df)
    show_df.to_csv('../../data/interim/fox-last-year-sent-comb.csv')
# show_df.to_csv('../../data/interim/cnn-last-year-sent-comb.csv')
