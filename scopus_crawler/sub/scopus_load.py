from pybliometrics.scopus import ScopusSearch
from pybliometrics.scopus.utils import config
import pandas as pd
import re

class ScopusCrawlerBest:
    def __init__(self, input_path='./sub_data/best_paper_awards_crawl.csv', output_path='./sub_data/best_paper_awards_scopus.csv', api_key='cc5139cb362dbf0aac149aabdfa4011f'):
        self.input_path = input_path
        self.output_path = output_path
        config['Authentication']['APIKey'] = api_key  # API 키 설정 필요
        config['Authentication']['InstToken'] = ''
        pd.set_option('display.max_columns', None)
    
    @staticmethod
    def keep_letters_and_digits(input_string):
        """영어 알파벳과 숫자를 제외한 모든 문자를 제거"""
        return re.sub(r'[^a-zA-Z0-9\'\,\.óàáâãäåçèéêëìíîïñòóôõöùúûü]', ' ', input_string).strip()
    
    def search_papers(self):
        """CSV에서 논문 데이터를 읽고 Scopus에서 검색하여 결과를 저장"""
        best_papers = pd.read_csv(self.input_path)
        only_first = best_papers.groupby(['year', 'paper']).first().reset_index()
        total_set = pd.DataFrame()
        not_done = []

        for row in only_first.iterrows() :
            paper = (row[1]['paper'].replace("(", "").replace(")", ""))
            paper = self.keep_letters_and_digits(paper)
            paper = paper.replace("  ", " ")
            author = (row[1]['author'].split(" "))
            if author[len(author)-1] != '': 
                author = author[len(author)-1]
            else :
                author = author[len(author)-2]

            out = ' TITLE-ABS-KEY ( ' + paper + ' ) AND AUTH ( ' + author + ' )' 

            s = ScopusSearch(out, download=True, # 검색 결과를 저장합니다. 
                            verbose=False)  # 진행 상황을 표시합니다.

            if s.get_results_size() == 0 :
                if author != self.keep_letters_and_digits(author) :
                    out = ' TITLE ( ' + paper + ' )'
                    s = ScopusSearch(out, download=True, # 검색 결과를 저장합니다. 
                        verbose=False)  # 진행 상황을 표시합니다.
                    if s.get_results_size() != 0 :
                        df_s = pd.DataFrame(s.results)
                        df_s = df_s.sort_values('citedby_count',ascending=False).head(1)
                        df_s['origin_ref'] = row[1]['conference']
                        total_set = pd.concat([total_set, df_s])
                        continue
                
                paper = paper.replace(" and ", " ")
                paper = paper.replace(" or ", " ")
                paper = paper.replace(" ", " AND ")

                out = ' TITLE ( ' + paper + ' ) '
                s = ScopusSearch(out, download=True, # 검색 결과를 저장합니다. 
                            verbose=False)  # 진행 상황을 표시합니다.
                
                if s.get_results_size() != 0 :
                    df_s = pd.DataFrame(s.results)
                    df_s['origin_ref'] = row[1]['conference']
                    df_s = df_s[df_s['coverDate'].str.startswith(str(row[1]['year']))]
                    df_s = df_s.sort_values('citedby_count',ascending=False).head(1)
                    total_set = pd.concat([total_set, df_s])
                    continue
                else :
                    not_done.append(row[1])
            elif s.get_results_size() == 1:
                df_s = pd.DataFrame(s.results)
                df_s['origin_ref'] = row[1]['conference']
                total_set = pd.concat([total_set, df_s])
            else :
                df_s = pd.DataFrame(s.results)
                if len(df_s[df_s['coverDate'].str.startswith(str(row[1]['year']))]) != 0 :
                    df_s = df_s[df_s['coverDate'].str.startswith(str(row[1]['year']))]
                    if len(df_s.loc[df_s['subtype']=='cp']) != 0 :
                        df_s = df_s.loc[df_s['subtype']=='cp']

                elif len(df_s.loc[df_s['subtype']=='cp']) != 0 :
                    df_s = df_s.loc[df_s['subtype']=='cp']

                df_s = df_s.sort_values('citedby_count',ascending=False).head(1)
                df_s['origin_ref'] = row[1]['conference']
                total_set = pd.concat([total_set, df_s])

        print(f"Best Awards : 전체 불러온 Paper 수: {len(total_set)}")
        print(f"Best Awards : 불러오지 못한 Paper 수: {len(not_done)}")
        total_set.to_csv(self.output_path, index=False)

