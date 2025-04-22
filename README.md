# UpDn - Ghat GPT를 활용한 기업의 주가 등락 예측 서비스 (Back-end application)

* 2023.09.20. - 2023.12.07.
* 2인 팀 프로젝트로 진행
<br><br><br>

# 개요

* 크롤링한 경제 뉴스 데이터를 기반으로, Prompt engineering을 활용하여 Chat GPT로 해당 기업의 주가 등락을 예측하는 서비스.
* 주식 투자자의 의사결정 과정에 신뢰성 있는 정보 제공과 경제 분야 뉴스 기사 접근성을 높일 수 있는 서비스.
* 단시간 내에 가치있는 주식/경제 정보를 얻을 수 있는 플랫폼 역할 수행.
* 주기적인 크롤링을 주로 담당하는 Back-end application.
<br><br>

# Architecture
![image](https://github.com/user-attachments/assets/f870c4b0-3d00-40a5-a79c-8cbb6f5c223e)
<br><br><br>

![image](https://github.com/user-attachments/assets/1670aa7e-d5d3-49ae-b5a4-4467326d1f59)
<br><br>

# ERD
![image](https://github.com/user-attachments/assets/8375c8f3-a691-410f-9abd-4fb85a6fec11)
<br><br>

# 사용기술

* ### Flask
  * 가벼우면서도 HTTP 요청/응답 처리에 필요한 기능을 충분히 지원하며, 주기적으로 크롤링 작업을 실시할 수 있는 환경을 제공한다고 판단하여 선택.

* ### MySql
  * 뉴스기사 텍스트는 물론, 발행 날짜, url, 경제 뉴스 세부분야 등의 데이터를 다양한 조건으로 조회/관리하기 위해 RDBMS가 필요하다 판단하여 선택.

* ### BeautifulSoup
  * 브라우저 조작이 필요한 복잡한 크롤링은 필요하지 않았으며, 기본적인 기능만으로도 타겟 웹사이트를 충분히 크롤링 할 수 있어 선택.
 
* ### BackgroundScheduler
  * 주기적인 크롤링 작업을 백그라운드에 등록하고, 실행 주기를 설정하기 위해 선택.
<br><br>

# 주요 개발내역

* ### 크롤링과 데이터 정제 구현 ([코드위치](https://github.com/yangsp31/UpDn-Flask-Server/blob/main/Crawling.py#L32))
  * 요청받은 html 데이터의 [dd, dt] 속성의 데이터중 {href, articleSummary}에 해당하는 데이터 추출 구현.
  * 추출한 데이터 내의 [span] 속성을 모두 제거한 형태의 데이터로 가공 후 text 반환 구현.
----
 
* ### DB에 정제된 데이터 저장 구현 ([코드위치](https://github.com/yangsp31/UpDn-Flask-Server/blob/main/Crawling.py#L50))
  * DB에 중복 저장을 방지하기 위해, 마지막으로 저장된 카테고리별 뉴스 기사의 URL을 조회하여 반환하도록 구현.
  * 저장할 데이터의 URL을 반환된 마지막으로 저장된 뉴스기사의 URL들과 비교하며 저장 구현.
  * DB에 Write 작업을 실행하는 동안, 데이터 무결성을 보장하기 위해 Lock을 적용.
<br><br>

# 회고 & 개선 필요사항/방법 (회고 원문 : [Velog](https://velog.io/@yang_seongp31/UpDn-Flask))

* ### Flask 선택
  * 프로젝트 구조를 보면, App에서 RealTimeData라는 실시간 환율과 최다 검색 기업명 데이터를 요청하고 SpringBoot는 이 요청을 크롤링을 진행하는 서버로 전달하여, 실시간으로 필요한 데이터를 크롤링 하여 App으로 전달하는 구조.
  * 이 구조 자체는 요청량이 늘어날수록 크롤링을 진행하는 서버의 부하가 높아지며, 최악의 경우엔 모든 요청을 정상적으로 처리가 불가하다 판단. 사실상 의미없는 웹서버를 하나 더 추가한 것이라 판단하기에 좋지않은 구조라 생각.
  * 요청량이 늘어나게 되면 모든 요청에 대해 실시간으로 계속 RealTimeData에 대한 크롤링을 새로 해야하기 떄문.
  * RealTimeData를 길지 않은 주기(최소 1분 ~ 최대 10분)로 크롤링하여 DB에 넣거나 Redis에 저장하고, 요청시에는 SpringBoot에서 검색하여 전달하는 구조로 구축 한다면 사용량이 늘어나도 이전의 구조보다는 불필요한 서버부담이 절감이 될것이라 판단.
  * 혹은 외부 API를 사용하여 Mobile application이 자체적으로 데이터를 얻는 방법을 사용 한다면 프로젝트 구조가 더욱 간결해 지고 불필요한 서버 부하도 상당히 절감될 것이라 판단.
  * 이러한 구조로 구축 한다면 의미없는 웹서버를 만들지 않고, 주기적으로 크롤링을 하여 DB에 데이터를 저장만 하는 Batch Server로 만들수 있어, 사실상 모든 요청은 SpringBoot에서 처리가 가능해진다 라고 생각.
  * 결론적으로, 의미없는 웹서버를 하나 더 넣은 것이기 때문에, 이 프로젝트에서 Flask 선택은 실패한 판단이라고 생각.
  <br>
 
   * 부하테스트 예시 자료 (로컬PC 환경에서 임의로 테스트한 결과임으로 실제와 오차가 존재할수 있음.)

  ![image](https://github.com/user-attachments/assets/42a7133c-701a-4655-aa23-9b20cf4d0a4b)
  <br>

  * 테스트용 Flask 로직
  ```
  import random
  import time

  app = Flask(__name__)

  # 최다 검색 기업명과 환율을 가정한 데이터 생성
  def generate_random_companies():
      companies = ["Company A", "Company B", "Company C", "Company D", "Company E"]
      return random.choice(companies)

  def generate_random_exchange_rates():
      return {
          "USD_TO_EUR": random.uniform(0.8, 1.2),
          "USD_TO_JPY": random.uniform(100, 150),
          "USD_TO_GBP": random.uniform(0.7, 1.0),
      }

  # 부하를 발생시키는 로직
  
  def simulate_heavy_load():
      # 일부러 CPU 부하를 발생시키는 루프
      result = []
      for _ in range(10000):  # 10000번 반복하여 계산량 증가
          result.append(generate_random_companies())
          result.append(generate_random_exchange_rates())
      return result

  @app.route('/', methods=['GET'])
  def start_load():
      try:
          data = simulate_heavy_load()

          # 부하 작업이 끝난 후 결과를 반환
          return jsonify({
              "status": "success",
              "data": data[:5],
          }), 200
      except Exception as e:
          return jsonify({'error': str(e)}), 500

  if __name__ == '__main__':
      app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
  ```

* ### 크롤링 타겟 데이터 선택
  * 이 프로젝트는 Chat GPT를 Prompt Engineering과 뉴스 기사를 기반으로 특정 기업의 주가 등락을 예측하는 서비스.
  * 하지만 이 프로젝트에서는 뉴스 기사 원문을 사용하지 않았음. 다양한 기사를 선택해야 데이터 편향을 줄일 수 있지만, 뉴스 기사의 텍스트는 길이가 상당히 길기 때문에, Prompt Engineering을 포함한 상태로 ChatGPT에 입력하기에는 한계가 있었기 때문.
  * 이러한 이유로 뉴스 기사 데이터는 뉴스 원문이 아닌 뉴스 기사들의 리스트에서 제목 밑에 출력되는 뉴스 기사 요약문, 또는 뉴스 기사 원문의 가장 앞에 위치한 문장의 일부라고 할수 있는 그리 길지 않은 텍스트를 사용.
  * 누락된 텍스트도 많고 특정 기업명과 사업 분야가 나타나지 않기도 하며, 가장 중요한 내용이 존재하지 않기도 하여, 적절하지 않은 데이터 선택임.
  * 데이터 정제시, BERTopic을 활용하면 뉴스 기사 본문에서 핵심 키워드를 추출해 짧은 텍스트로 정리할 수 있으며, 기업 정보뿐 아니라 사업 분야 데이터까지 함께 활용함으로써 더 신뢰도 높은 예측이 가능하다고 판단.
  * 결과적으로, DB 저장과 검색의 과정을 좀 더 효율적으로 진행할 수 있으며, Chat GPT의 입력 제한 안에서 보다 다양한 뉴스 기사의 데이터를 최대한 입력하여 더욱 질 높은 예측을 가능하게 할 수도 있을 것이라 예상.
 
* ### DB 저장 전략
  * 크롤링한 데이터를 DB에 저장하는 프로세스가 진행 중일 때, App에서 특정 기업에 대한 예측 요청이 들어오면 최신 데이터가 반영되지 않는 문제에 대해 고민함.
  * 그 결과, 크롤링한 데이터를 DB에 저장하기 전, 저장할 테이블에 Lock을 걸고 모든 데이터가 저장되었을때 UnLock을 진행 후, Commit을 진행하는 방식으로 구축.
  * 하지만, 트랜잭션 단위로 Lock을 거는것이 아니라 테이블 자체에 Lock을 거는 방식이기 떄문에 Flask에서 DB에 데이터를 쓰고 있는 중일때 Spring Boot에서 DB에 데이터 접근시, 병목현상이 발생.
  * 실시간 데이터 반영이 중요하더라도, 테이블 단위의 Lock은 DB 접근에 경직성이 발생하고 동시성을 낮추므로, 트랜잭션 기반으로 저장 전략을 구축하는 것이 적절하다고 판단. 
  * 테이블 전체에 Lock을 거는 방식이 아닌, 트랜잭션 안에서 Commit 타이밍을 일정량의 데이터가 저장될때마다 진행하여, 동시성을 높이고 병목 현상도 완화하면서, 최신 데이터 누락문제를 최소화 할 수 있다고 판단.
  * 프로젝트가 최신 데이터를 엄밀히 요구하는 경우, 테이블 Lock을 사용해 동시성 충돌을 막을 수 있음.
  * 그러나 DB 구조상 각 기업이나 사업분야별로 데이터를 구분하여 관리하지 않고 하나의 테이블 안에서 모두 관리하기 때문에 때문에, Lock 사용 시 병목 현상이 발생하고 동시성도 낮아지게 됨.
  * 따라서, 데이터베이스 구조와 데이터 유형을 변경하지 않는 한, 테이블 Lock은 적합하지 않은 해결책이라 판단.
<br><br>
 
* ### 개선 필요사항/방법
  * RealTimeData를 DB 또는 Redis에 길지 않은 주기(1분 ~ 10분)로 수집하여 관리하는 구조로 교체하여 Flask 서버에서 주기적인 클로링 작업만 진행하는 Batch 서버로 교체.
  * BERTopic을 활용하면 뉴스 기사 본문에서 핵심 키워드를 추출해 짧은 텍스트로 정제하고 관리.
  * 트랜잭션 안에서 Commit 타이밍을 일정량의 데이터가 저장될때마다 진행하거나, 데이터 유형과 DBMS 구조를 변경하여 테이블 Lock, 또는 비관적 Lock(PESSIMISTIC_WRITE)을 사용.


