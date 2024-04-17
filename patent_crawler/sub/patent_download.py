import requests
import zipfile
import os
from tqdm import tqdm

class ZipDownloader:
    def __init__(self, urls = [], extract_to='./sub_data'):
        """
        ZipDownloader 클래스 생성자.

        Args:
        urls (list of str): 다운로드할 ZIP 파일들의 URL 목록입니다.
        extract_to (str): 압축을 풀 폴더의 경로입니다.
        """
        self.urls = urls
        if len(self.urls) == 0 :
                self.urls = ['https://s3.amazonaws.com/data.patentsview.org/download/g_application.tsv.zip',
                    'https://s3.amazonaws.com/data.patentsview.org/download/g_inventor_disambiguated.tsv.zip',
                    'https://s3.amazonaws.com/data.patentsview.org/download/g_cpc_current.tsv.zip',
                    'https://s3.amazonaws.com/data.patentsview.org/download/g_location_disambiguated.tsv.zip',
                    'https://s3.amazonaws.com/data.patentsview.org/download/g_patent.tsv.zip',
                    'https://s3.amazonaws.com/data.patentsview.org/download/g_assignee_disambiguated.tsv.zip',
                    'https://bulkdata.uspto.gov/data/patent/ai/landscape/economics/2020/ai_model_predictions.tsv.zip'] 
        self.extract_to = extract_to

    def download_and_unzip(self, url):
        """
        URL에서 ZIP 파일을 다운로드하고, 진행 상태를 표시하며, 압축을 풀고, ZIP 파일을 삭제합니다.

        Args:
        url (str): 다운로드할 ZIP 파일의 URL입니다.
        """
        # ZIP 파일 이름을 URL에서 추출합니다.
        zip_name = url.split('/')[-1]
        zip_path = os.path.join(self.extract_to, zip_name)
        
        if os.path.exists(zip_path[:-4]):
            print(f"File already exists: {zip_path[:-4]}, skipping download.")
            return

        # 서버로부터 ZIP 파일의 사이즈를 알아내기 위해 HEAD 요청을 보냅니다.
        response = requests.head(url)
        file_size = int(response.headers.get('content-length', 0))

        # 서버로부터 ZIP 파일을 스트림 모드로 가져옵니다.
        print(f"Downloading ZIP file... : {zip_name}")
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 오류가 있을 경우 예외를 발생시킵니다.

        # 진행 상태 표시를 위한 tqdm 설정
        progress = tqdm(total=file_size, unit='iB', unit_scale=True)

        # ZIP 파일을 로컬에 저장합니다.
        with open(zip_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
                progress.update(len(chunk))
        progress.close()

        # ZIP 파일 압축 해제
        print(f"Unzipping the file... : {zip_name}")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.extract_to)

        # 원본 ZIP 파일 삭제
        print(f"Deleting the ZIP file... : {zip_name}")
        os.remove(zip_path)
        print("Process completed successfully.")

    def run(self):
        """모든 URL에 대해 다운로드 및 압축 해제를 실행합니다."""
        for url in self.urls:
            self.download_and_unzip(url)