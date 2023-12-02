from flask import Flask
import RealTimeCrawling as RTC
import Crawling as CL
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# CL.get_all_news_titles() 함수를 Flask 서버 스케쥴러에 등록
def scheculed_job() :
    CL.get_all_news_data()

# Flask서버에서 실시간 데이터 전달 요청을 처리하는 엔드포인트/함수 
@app.route('/Flask/realtimeData')
def home() :
    return RTC.RTCrawling()         # RTC.RTCrawling() = 실시간으로 페이지에서 크롤링한 데이터를 반환 

if __name__ == '__main__' :
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheculed_job, 'interval', hours = 2)         # Flask 서버 스케쥴러에 등록된 CL.get_all_news_titles() 함수를 2시간 주기로 실행함으로 설정
    scheduler.start()

    app.run('0.0.0.0', port=5000, debug=True)         # 해당 주소와 포트번호로 Flask서버 실행
