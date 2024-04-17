from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

class BestPaperAwardsCrawler:
    def __init__(self, url='https://jeffhuang.com/best_paper_awards/#2023', output_path='./sub_data/best_paper_awards_crawl.csv'):
        self.url = url
        self.output_path = output_path

    def fetch_data(self):
        """URL에서 데이터를 가져오기"""
        response = requests.get(self.url)
        if response.status_code != 200:
            raise ValueError('Request Failed!')
        return response.text

    def parse_html(self, html):
        """HTML을 파싱하여 데이터를 추출"""
        soup = BeautifulSoup(html, 'html.parser')
        data = []
        year = None
        for row in soup.find_all('tr'):
            cols = row.find_all(['th', 'td'])
            if len(cols) == 1:
                year = cols[0].text.strip()
                continue
            elif len(cols) == 3:
                conference = cols[0].text.strip()
                cols = cols[1:]

            paper = cols[0].text.strip()
            authors = self.parse_authors(cols[1])
            for author in authors:
                data.append([year, conference, paper] + author)

        return data

    def parse_authors(self, author_col):
        """저자 정보 파싱"""
        authors_data = []
        try:
            first = [author_col.text.split(";")[0]]
            extra_tags = re.split(r'<br/>', str((author_col.find_all("div")[0])))
            extra_tags[0] = extra_tags[0][extra_tags[0].find(">")+1:]
            extra_tags[-1] = extra_tags[-1][:extra_tags[-1].find("<")]
            first = first + extra_tags
        except:
            first = [author_col.text.split(";")[0]]

        for author_info in first:
            authors = author_info.split(", ")
            if "&" in authors[0]:
                authors[0] = authors[0].replace(" & ", " &").split(" &")
                for author in authors[0]:
                    authors_data.append([author, authors[1]])
            else:
                authors_data.append([authors[0], authors[1]])

        return authors_data

    def save_data(self, data):
        """데이터를 CSV 파일로 저장"""
        columns = ['year', 'conference', 'paper', 'author', 'institute']
        df = pd.DataFrame(data, columns=columns)
        df.to_csv(self.output_path, index=False)

    def run(self):
        """크롤링 실행"""
        html = self.fetch_data()
        data = self.parse_html(html)
        self.save_data(data)