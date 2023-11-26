import requests
from bs4 import BeautifulSoup

def RTCrawling() : 
    url_exchange = 'https://m.stock.naver.com/marketindex/home/exchangeRate/exchange'
    response_exchange = requests.get(url_exchange)
    soup_exchange = BeautifulSoup(response_exchange.text, 'html.parser')

    exchange_rates = {}
    for strong_tag in soup_exchange.find_all('strong', class_='MainListItem_name__2Nl6J'):
        currency_name = strong_tag.text.strip()
        if currency_name in ['미국 USD', '일본 JPY']:
            exchange_rate = strong_tag.find_next_sibling('span', class_='MainListItem_price__dP8R6').text.strip()
            exchange_rates[currency_name] = exchange_rate

    url_company = 'https://finance.naver.com/news/news_list.naver?mode=LSS3D&section_id=101&section_id2=258&section_id3=406'
    response_company = requests.get(url_company)
    soup_company = BeautifulSoup(response_company.text, 'html.parser')

    data_dict = {}
    rank = 1
    for a_tag in soup_company.find_all('td'):
        company_tag = a_tag.find('a', class_='company')
        if company_tag:
            company_name = company_tag.text.strip()
            data_dict[f'{rank}등'] = company_name
            rank += 1

    result = [exchange_rates, data_dict]

    return result