from flask import Flask
import RealTimeCrawling as RTC
import Crawling as CL
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

def scheculed_job() :
    CL.get_all_news_titles()

@app.route('/Flask/realtimeData')
def home() :
    return RTC.RTCrawling()

if __name__ == '__main__' :
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheculed_job, 'interval', hours = 1)
    scheduler.start()

    app.run('0.0.0.0', port=5000, debug=True)
