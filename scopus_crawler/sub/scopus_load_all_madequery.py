from pybliometrics.scopus import ScopusSearch
from pybliometrics.scopus.utils import config
import pandas as pd
import re

class ScopusCrawlerQuery:
    def __init__(self, data_path='./sub_data/query.csv', output_path='./sub_data/best_scopus_predefined.csv', api_key='cc5139cb362dbf0aac149aabdfa4011f'):
        self.data_path = data_path
        self.output_path = output_path
        config['Authentication']['APIKey'] = api_key  # API 키 설정 필요
        config['Authentication']['InstToken'] = ''
        pd.set_option('display.max_columns', None)

    @staticmethod
    def keep_letters_and_digits(input_string):
        """영어 알파벳과 숫자를 제외한 모든 문자를 제거"""
        return re.sub(r'[^a-zA-Z0-9\'\,\.óàáâãäåçèéêëìíîïñòóôõöùúûü]', ' ', input_string).strip()

    def run_queries(self):
        """쿼리 파일을 로드하고 Scopus에서 각 쿼리를 실행한 후 결과를 저장"""
        query_df = pd.read_csv(self.data_path)
        whole_conference = pd.DataFrame()

        for index, row in query_df.iterrows():
            q = row[1]
            ref = row[0]
            s = ScopusSearch(q, download=True, verbose=True)
            if s.get_results_size() != 0:
                df_s = pd.DataFrame(s.results)
                df_s = df_s.loc[(df_s['subtype'] == 'cp') | (df_s['subtype'] == 'ar')]
                df_s['origin_ref'] = ref
                whole_conference = pd.concat([whole_conference, df_s], ignore_index=True)
                print("Total Length:", len(df_s), "Conference Name:", ref)

        whole_conference.to_csv(self.output_path, index=False)