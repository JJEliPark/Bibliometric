import pandas as pd

class PatentDataProcessor:
    def __init__(self, data_directory='./sub_data'):
        self.data_directory = data_directory
        self.load_data()

    def load_data(self):
        """데이터를 불러오는 메소드"""
        self.data_inv = pd.read_csv(f"{self.data_directory}/g_inventor_disambiguated.tsv", delimiter='\t', keep_default_na=False)
        self.data_loc = pd.read_csv(f"{self.data_directory}/g_location_disambiguated.tsv", delimiter='\t', keep_default_na=False)
        self.data_patent = pd.read_csv(f"{self.data_directory}/g_patent.tsv", delimiter='\t', keep_default_na=False)
        self.data_assign = pd.read_csv(f"{self.data_directory}/g_assignee_disambiguated.tsv", delimiter='\t', keep_default_na=False)
        self.data_ai_model = pd.read_csv(f"{self.data_directory}/ai_model_predictions.tsv", delimiter='\t', keep_default_na=False)
        self.data_app = pd.read_csv(f"{self.data_directory}/g_application.tsv", delimiter='\t', keep_default_na=False)
        self.filter_ai_data()

    def filter_ai_data(self):
        """AI 관련 특허 데이터를 필터링하는 메소드"""
        self.data_ai_model = self.data_ai_model.loc[self.data_ai_model['predict50_any_ai'] == 1]
        self.data_ai = pd.merge(self.data_ai_model, self.data_app, left_on='appl_id', right_on='application_id', how='inner')
        self.data_ai = self.data_ai[['patent_id', 'application_id']].drop_duplicates()

    def merge_data_by_inventors(self):
        """발명가 기준으로 데이터 병합"""
        data3 = pd.merge(self.data_inv, self.data_ai, on='patent_id', how='inner')
        data3 = pd.merge(data3, self.data_loc, on='location_id', how='inner')
        data3 = pd.merge(data3, self.data_patent, on='patent_id', how='left')
        data3 = data3.sort_values(['patent_id', 'inventor_sequence'])
        return data3

    def merge_data_by_assignees(self):
        """양수인 기준으로 데이터 병합"""
        data_4 = pd.merge(self.data_assign, self.data_ai, on='patent_id', how='inner')
        data_4 = pd.merge(data_4, self.data_loc, on='location_id', how='inner')
        self.data_patent['patent_id'] = self.data_patent['patent_id'].astype(str)
        data_4 = pd.merge(data_4, self.data_patent, on='patent_id', how='left')
        data_4 = data_4.sort_values(['patent_id', 'assignee_sequence'])
        return data_4
