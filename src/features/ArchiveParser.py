import re
import xml.etree.ElementTree as ET
import pandas as pd
from bs4 import BeautifulSoup


class ArchiveParser:
    def __init__(self, file_list, meta_path, html_path):
        self.file_list = file_list
        self.meta_path = meta_path
        self.html_path = html_path

    def parse_program(self, identifier):
        html = self.html_path + "/" + identifier + '.html'
        meta = self.meta_path + "/" + identifier + '_meta.xml'
        show_pattern = re.compile('(_[A-z,\.]+\d*)')
        find_all = re.findall(show_pattern, identifier)
        show_name = find_all[0][1:]
        print(show_name)
        contributor, runtime, start_time, stop_time = '', '', '', ''
        subjects = []
        time_stamps = []
        text_blocks = []
        show = []
        p = re.compile('(?!start)\d+')
        try:
            with open(meta) as xdoc:
                print(meta)
                tree = ET.parse(xdoc)
                root = tree.getroot()
                for child in root:
                    # print(child.tag, child.text)
                    if child.tag == 'contributor':
                        contributor = child.text
                    elif child.tag == 'runtime':
                        runtime = child.text
                    elif child.tag == 'start_time':
                        start_time = child.text
                    elif child.tag == 'stop_time':
                        stop_time = child.text
                    elif child.tag == 'subject':
                        subjects.append(child.text)

            with open(html, encoding="utf8") as fp:
                print(html)
                soup = BeautifulSoup(fp, features='html.parser')
                for div in soup.find_all('div', class_='th'):
                    time_stamp = div.find('a').get('href')
                    find_all = re.findall(p, time_stamp)
                    start = find_all[0]
                    end = find_all[1]
                    time_stamps.append({'start_snip': start, 'end_snip': end})
                for div in soup.find_all('div', class_='snippet'):
                    text_blocks.append(div.get_text().strip())

            for i in range(0, len(time_stamps)):
                snip_dict = time_stamps[i]
                snip_dict['snippet'] = text_blocks[i]
                snip_dict['contributor'] = contributor
                snip_dict['runtime'] = runtime
                snip_dict['start_time'] = start_time
                snip_dict['stop_time'] = stop_time
                snip_dict['identifier'] = identifier
                snip_dict['subjects'] = subjects
                snip_dict['show_name'] = show_name
                show.append(snip_dict)
        except IOError:
            print('Cannot open {} or {}'.format(meta, html))
        except:
            print('Parsing error')
        finally:
            return show

    def parse_file_list(self):
        shows = []
        try:
            identifiers = pd.read_csv(self.file_list)
        except IOError:
            print('Cannot open {}'.format(self.file_list))
        for index, row in identifiers.iterrows():
            shows = shows + self.parse_program(identifier=row['identifier'])

        return pd.DataFrame(shows)
