# 프로젝트 제목

이 프로젝트는 Scopus API와 USPTO 데이터를 활용하여 연구 데이터를 수집하고 가공하는 스크립트를 제공합니다.

## 설치 방법

이 프로젝트를 사용하기 전에 필요한 환경과 도구를 설치해야 합니다. 다음 단계에 따라 설치를 진행하세요.

### 필수 조건

- Python 3.8 이상
- 필요한 Python 라이브러리: `requests`, `json`, `pandas` 등

### 설치

1. 이 저장소를 클론하거나 다운로드합니다:
```git clone https://github.com/JJEliPark/Bibliometric.git```

2. 필요한 라이브러리를 설치합니다:
```pip install -r requirements.txt```


## 사용 방법

### Scopus 데이터 수집

1. Scopus API 키를 확보하세요. (Scopus 등록 및 API 키 발급 방법은 [Scopus API Documentation](https://www.scopus.com) 참조)
2. `scopus_data.py` 스크립트를 실행하여 데이터를 수집합니다:
```python scopus_data.py```


### USPTO 데이터 수집

1. USPTO의 데이터 접근 권한을 확인하세요. (USPTO 데이터 사용 방법은 [USPTO Data Access](https://www.uspto.gov) 참조)
2. `uspto_data.py` 스크립트를 실행하여 데이터를 수집합니다:
```python uspto_data.py```

## 기여하기

이 프로젝트에 기여하고 싶으시다면, 풀 리퀘스트를 보내거나 이슈를 등록해 주세요.

## 라이센스

이 프로젝트는 [MIT 라이센스](LICENSE) 하에 배포됩니다.

## 저자

- [pkmon1d@snu.ac.kr]

## 참고 자료

- Scopus API 공식 문서: https://www.scopus.com
- USPTO 데이터 접근: https://www.uspto.gov
