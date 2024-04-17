from pybliometrics.scopus import ScopusSearch
from pybliometrics.scopus.utils import config
import pandas as pd
import re

class ScopusCrawlerAll:
    def __init__(self, input_path = './sub_data/best_paper_awards_scopus.csv', output_path='./sub_data/best_scopus_whole.csv' , api_key='cc5139cb362dbf0aac149aabdfa4011f'):
        # API 키 설정
        config['Authentication']['APIKey'] = api_key
        config['Authentication']['InstToken'] = ''
        self.input_path = input_path
        self.output_path = output_path
    
    @staticmethod
    def keep_letters_and_digits(input_string):
        """영어 알파벳(a-zA-Z), 숫자(0-9) 및 일부 특수문자를 제외한 모든 문자 제거"""
        return re.sub(r'[^a-zA-Z0-9\'\,\.óàáâãäåçèéêëìíîïñòóôõöùúûü]', ' ', input_string).strip()

    def load_data(self):
        """데이터 로드 및 초기 처리"""
        total_set = pd.read_csv(self.input_path)

        total_set = total_set[['publicationName', 'origin_ref']].drop_duplicates()
        total_set = total_set.loc[total_set['publicationName'] != 'Artificial Intelligence']
        total_set = total_set.loc[total_set['publicationName'] != 'Computer Networks']
        total_set = total_set.loc[total_set['publicationName'] != 'Machine Learning']
        total_set = total_set.loc[total_set['publicationName'] != 'SAE Technical Papers']
        total_set = total_set.loc[total_set['publicationName'] != 'CEUR Workshop Proceedings']
        total_set = total_set.loc[total_set['publicationName'] != 'ACM International Conference Proceeding Series']
        total_set = total_set.loc[total_set['publicationName'] != 'Proceedings of Machine Learning Research']


        total_set = total_set.loc[~total_set['publicationName'].str.contains("Lecture Notes")]
        total_set = total_set.drop_duplicates(subset='publicationName')
        return total_set

    def run_search(self):
        """Scopus 검색 실행 및 데이터 수집"""
        total_set = self.load_data()
        whole_conference = pd.DataFrame()
        for row in total_set.iterrows() :
            query = "SRCTITLE ("
            art = self.keep_letters_and_digits(row[1][0])
            art = art.replace("  ", " ")
            query = query + art + ") AND PUBYEAR > 1995 AND PUBYEAR < 2024 " 
            s = ScopusSearch(query, download=True, # 검색 결과를 저장합니다. 
                            verbose=True)  # 진행 상황을 표시합니다.
            if s.get_results_size() != 0 :
                df_s = pd.DataFrame(s.results)
                df_s = df_s.loc[(df_s['subtype']=='cp') | (df_s['subtype']=='ar')]
                df_s['origin_ref'] = row[1][1]
                whole_conference = pd.concat([whole_conference, df_s])
                print("Total Length:", len(df_s), "Conference Name: " ,row[1][1])

        whole_conference = whole_conference.drop_duplicates(subset='eid')
        whole_conference.to_csv(self.output_path, index=False)
