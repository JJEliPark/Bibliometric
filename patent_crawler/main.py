import pandas as pd
from sub.patent_download import ZipDownloader
from sub.patent_merge import PatentDataProcessor




def main():
    # 스크립트 순서대로 실행
    downloader = ZipDownloader()
    downloader.run()
    print("*******Download Completed")

    processor = PatentDataProcessor()
    data_by_inventors = processor.merge_data_by_inventors()
    data_by_inventors.to_csv('../data/ai_patent_inventors.csv', index=False)
    print("*******ai_patent_inventors.csv Created.")

    data_by_assignees = processor.merge_data_by_assignees()
    data_by_assignees.to_csv('../data/ai_patent_assignees.csv', index=False)
    print("*******ai_patent_assignees.csv Created.")

    # BestPaperAwardsCrawler 클래스 인스턴스화 및 실행

if __name__ == "__main__":
    main()