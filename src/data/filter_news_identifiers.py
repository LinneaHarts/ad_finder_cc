import click
import csv
import pandas as pd

from datetime import datetime, timedelta


@click.command()
@click.option('--network', help='Network to download news from', default='FOXNEWS')
@click.option('--start_date', help='Start date for getting closed captions in the format YYYYMMDD',
              default='20200101')
@click.option('--end_date', help='End date for getting closed captions in the format YYYYMMDD',
              default='20200101')
@click.option('--input_file', help='Path to search input file', default='../../data/raw/search.csv')
@click.option('--output_file', help='Path to search output file', default='../../data/raw/search-filtered.csv')
def filter_news_identifiers(network, start_date, end_date, input_file, output_file):
    programs = pd.read_csv(input_file)
    start_date_obj = datetime.strptime(start_date, '%Y%m%d')
    end_date_obj = datetime.strptime(end_date, '%Y%m%d')

    # construct list of dates encompassing the range between start date and end date
    date_strings = []
    temp_date = start_date_obj
    while temp_date <= end_date_obj:
        date_strings.append(temp_date.strftime('%Y%m%d'))
        temp_date = temp_date + timedelta(days=1)

    program_list = []
    for date_string in date_strings:
        program_list = program_list + list(programs[programs.identifier.str.contains('_{}'.format(date_string)) &
                                                    programs.identifier.str.contains(network)]['identifier'])
        print(date_string)

    filtered_programs_df = pd.DataFrame(program_list)
    filtered_programs_df.columns = ['identifier']
    filtered_programs_df.to_csv(output_file, index=False)

    print(program_list)
    print('Filtering completed')


if __name__ == "__main__":
    filter_news_identifiers()
