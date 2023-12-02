import requests
from bs4 import BeautifulSoup
import pymysql
import datetime
import SearchURL
import TextExtraction

def get_all_news_data():    # 크롤링 진행 대상 페이지 URL 모음
    urls = [
        'https://finance.naver.com/news/news_list.naver?mode=LSS3D&section_id=101&section_id2=258&section_id3=401',
        'https://finance.naver.com/news/news_list.naver?mode=LSS3D&section_id=101&section_id2=258&section_id3=402',
        'https://finance.naver.com/news/news_list.naver?mode=LSS3D&section_id=101&section_id2=258&section_id3=406'
    ]
    url_index = 0

    # DB(Mysql) 에 연결하여 DB사용 준비
    DB = pymysql.connect(host = '127.0.0.1', user = 'root', password = 'Zxc.44040', db = 'updn_db', charset = 'utf8')
    cursor = DB.cursor()
    now_date = datetime.datetime.now().strftime('%Y-%m-%d')

    # DB에 데이터 저장시 중복 데이터 저장을 회피하기 위한 마지막 크롤링 데이터 확인
    A1_urls = SearchURL.get_A1_urls(cursor)
    A2_urls = SearchURL.get_A2_urls(cursor)
    A3_urls = SearchURL.get_A3_urls(cursor)

    while url_index < 3 :
        current_page = 1

        while True :

            # 크롤링 할 페이지에 해당하는 URL선택 후 데이터 요청
            full_url = f'{urls[url_index]}&page={current_page}'
            response = requests.get(full_url)
            soup = BeautifulSoup(response.text, 'html.parser')      # 요청받은 데이터의 html 데이터을 추출 

            news_elements = soup.find_all(['dd', 'dt'], class_='articleSubject')

            # 요청받은 html 데이터의 [dd, dt] 속성의 데이터가 없을경우 처리 로직
            if not news_elements:
                url_index += 1
                break

            # 요청받은 html 데이터의 [dd, dt] 속성의 데이터중 {href, articleSummary}에 해당하는 데이터 추출후 DB에 저장
            for element in news_elements:
                news_url = element.find('a').attrs['href']
                summary_element = element.find_next_sibling('dd', class_ = 'articleSummary')
                news_summary = TextExtraction.get_article_summary(summary_element)  # 추출한 articleSummary 데이터 가공


                if news_summary : 
                    if (url_index == 0) :
                        try : 
                             if news_url not in A1_urls : 
                                 cursor.execute("LOCK TABLES article_data WRITE;")  # Flask 서버에서 크롤링 진행 후 DB에 Write 작업 실행 중 해당 DB에 데이터 무결성을 보장하기 위한 Lock 적용
                                 sql = "INSERT INTO article_data (publication_date, article_summary, url, category) VALUES (%s, %s, %s, %s)"
                                 cursor.execute(sql, (now_date, news_summary, news_url, 'A1'))
                        except Exception as e :    # DB에 Write 요청에 대한 오류 발생시 처리 로직
                            print(f"오류 : {e}")
                            cursor.execute("UNLOCK TABLES;")
                            DB.close()
                            return

                    elif(url_index == 1) :
                        try : 
                            if news_url not in A2_urls :
                                 sql = "INSERT INTO article_data (publication_date, article_summary, url, category) VALUES (%s, %s, %s, %s)"
                                 cursor.execute(sql, (now_date, news_summary, news_url, "A2"))
                        except Exception as e :    # DB에 Write 요청에 대한 오류 발생시 처리 로직
                            print(f"오류 : {e}")
                            cursor.execute("UNLOCK TABLES;")
                            DB.close()
                            return

                    else : 
                        try : 
                             if news_url not in A3_urls :
                                 sql = "INSERT INTO article_data (publication_date, article_summary, url, category) VALUES (%s, %s, %s, %s)"
                                 cursor.execute(sql, (now_date, news_summary, news_url, "A3"))
                        except Exception as e :    # DB에 Write 요청에 대한 오류 발생시 처리 로직
                            print(f"오류 : {e}")
                            cursor.execute("UNLOCK TABLES;")
                            DB.close()
                            return
                        finally :
                            cursor.execute("UNLOCK TABLES;") # 모든 데이터를 DB에 Write한 후 Lock 해제
                            
            current_page += 1

    DB.commit()    #DB에 Write 요청 commit 진행 (실질적으로 DB에 요청한 내용 모두 저장)
    DB.close()     #DB와 연결 해제