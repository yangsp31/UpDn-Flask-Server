import requests
from bs4 import BeautifulSoup
import pymysql
import datetime
import SearchURL

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
    company_urls = SearchURL.get_company_urls(cursor)
    M1_market_urls = SearchURL.get_M1_market_urls(cursor)
    M2_market_urls = SearchURL.get_M2_market_urls(cursor)

    while url_index < 3 :
        current_page = 1

        while True :
            full_url = f'{urls[url_index]}&page={current_page}'
            response = requests.get(full_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            news_elements = soup.find_all(['dd', 'dt'], class_='articleSubject')
            print(news_elements)

            if not news_elements:
                url_index += 1
                break

            for element in news_elements:
                news_title = element.find('a').text.strip()
                news_url = element.find('a').attrs['href']

                if (url_index == 0) :
                    try : 
                         if news_url not in M1_market_urls : 
                             cursor.execute("LOCK TABLES market_article WRITE;")
                             sql = "INSERT INTO market_article (publication_date, article_title, url, category) VALUES (%s, %s, %s, %s)"
                             cursor.execute(sql, (now_date, news_title, news_url, 'M1'))
                    except Exception as e :
                        print(f"오류 : {e}")
                        cursor.execute("UNLOCK TABLES;")
                        DB.close()
                        return

                elif(url_index == 1) :
                    try : 
                        if news_url not in M2_market_urls :
                             sql = "INSERT INTO market_article (publication_date, article_title, url, category) VALUES (%s, %s, %s, %s)"
                             cursor.execute(sql, (now_date, news_title, news_url, "M2"))
                    except Exception as e :
                        print(f"오류 : {e}")
                        cursor.execute("UNLOCK TABLES;")
                        DB.close()
                        return
                    finally : 
                        cursor.execute("UNLOCK TABLES;")

                else : 
                    try : 
                         if news_url not in company_urls :
                             cursor.execute("LOCK TABLES company_article WRITE;")
                             sql = "INSERT INTO company_article (publication_date, article_title, url) VALUES (%s, %s, %s)"
                             cursor.execute(sql, (now_date, news_title, news_url))
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