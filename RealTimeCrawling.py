import requests
from bs4 import BeautifulSoup

# 실시간으로 N Pay증권 페이지에서 USD, JPY 현재가/현재 최다 검색 기업명을 크롤링 하여 반환
def RTCrawling() : 
    url_exchange = 'https://m.stock.naver.com/marketindex/home/exchangeRate/exchange'
    response_exchange = requests.get(url_exchange)    # 해당 URL을 이용하여 크롤링 대상 페이지 요청
    soup_exchange = BeautifulSoup(response_exchange.text, 'html.parser')    # 요청받은 페이지의 html 데이터만을 추출

    # USD, JPY 현재가 html 데이터 안에서 추출 후 리스트에 입력
    exchange_rates = []
    for strong_tag in soup_exchange.find_all('strong', class_='MainListItem_name__2Nl6J'):
        currency_name = strong_tag.text.strip()
        if currency_name in ['미국 USD', '일본 JPY']:
            exchange_rate = strong_tag.find_next_sibling('span', class_='MainListItem_price__dP8R6').text.strip()
            exchange_rates.append(exchange_rate)

    url_company = 'https://finance.naver.com/news/news_list.naver?mode=LSS3D&section_id=101&section_id2=258&section_id3=406'
    response_company = requests.get(url_company)     # 해당 URL을 이용하여 크롤링 대상 페이지 요청
    soup_company = BeautifulSoup(response_company.text, 'html.parser')       # 요청받은 데이터의 html 데이터을 추출

    # 현재 최다 검색 기업명을 html 데이터 안에서 추출 후 리스트에 입력
    data_dict = []
    rank = 1
    for a_tag in soup_company.find_all('td'):
        company_tag = a_tag.find('a', class_='company')
        if company_tag:
            company_name = company_tag.text.strip()
            data_dict.append(company_name)
            rank += 1

    result = {'rate' : exchange_rates, 'nowRank' : data_dict}      # 추출한 USD, JYP 현재가와 현재 최다 검색 기업명이 각각 저장된 리스트를 Dictionary를 이용하여 취합(json 형식과 같음)

    return result # 추출한 모든 데이터 취합후 반환 (반환 형태 : Dictionary[= json])