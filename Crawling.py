import requests
from bs4 import BeautifulSoup
import pymysql
import datetime
import SearchURL
import TextExtraction

def get_all_news_titles():
    urls = [
        'https://finance.naver.com/news/news_list.naver?mode=LSS3D&section_id=101&section_id2=258&section_id3=401',
        'https://finance.naver.com/news/news_list.naver?mode=LSS3D&section_id=101&section_id2=258&section_id3=402',
        'https://finance.naver.com/news/news_list.naver?mode=LSS3D&section_id=101&section_id2=258&section_id3=406'
    ]
    url_index = 0
    DB = pymysql.connect(host = '127.0.0.1', user = 'root', password = 'Zxc.44040', db = 'updn_db', charset = 'utf8')
    cursor = DB.cursor()
    now_date = datetime.datetime.now().strftime('%Y-%m-%d')
    A1_urls = SearchURL.get_A1_urls(cursor)
    A2_urls = SearchURL.get_A2_urls(cursor)
    A3_urls = SearchURL.get_A3_urls(cursor)

    while url_index < 3 :
        current_page = 1

        while True :
            full_url = f'{urls[url_index]}&page={current_page}'
            response = requests.get(full_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            news_elements = soup.find_all(['dd', 'dt'], class_='articleSubject')

            if not news_elements:
                url_index += 1
                break

            for element in news_elements:
                news_url = element.find('a').attrs['href']
                summary_element = element.find_next_sibling('dd', class_ = 'articleSummary')
                news_summary = TextExtraction.get_article_summary(summary_element)

                if news_summary : 
                    if (url_index == 0) :
                        try : 
                             if news_url not in A1_urls : 
                                 cursor.execute("LOCK TABLES article_data WRITE;")
                                 sql = "INSERT INTO article_data (publication_date, article_summary, url, category) VALUES (%s, %s, %s, %s)"
                                 cursor.execute(sql, (now_date, news_summary, news_url, 'A1'))
                        except Exception as e :
                            print(f"오류 : {e}")
                            cursor.execute("UNLOCK TABLES;")
                            DB.close()
                            return

                    elif(url_index == 1) :
                        try : 
                            if news_url not in A2_urls :
                                 sql = "INSERT INTO article_data (publication_date, article_summary, url, category) VALUES (%s, %s, %s, %s)"
                                 cursor.execute(sql, (now_date, news_summary, news_url, "A2"))
                        except Exception as e :
                            print(f"오류 : {e}")
                            cursor.execute("UNLOCK TABLES;")
                            DB.close()
                            return

                    else : 
                        try : 
                             if news_url not in A3_urls :
                                 sql = "INSERT INTO article_data (publication_date, article_summary, url, category) VALUES (%s, %s, %s, %s)"
                                 cursor.execute(sql, (now_date, news_summary, news_url, "A3"))
                        except Exception as e : 
                            print(f"오류 : {e}")
                            cursor.execute("UNLOCK TABLES;")
                            DB.close()
                            return
                        finally :
                            cursor.execute("UNLOCK TABLES;")
                            
            current_page += 1

    DB.commit()
    DB.close()