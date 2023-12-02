import datetime

# DB에 데이터 저장시 중복저장을 회피하기 위해 마지막으로 저장된 {category = A1, publication_date = 현재날짜} 의 데이터의 URL 받아옴
def get_A1_urls(cursor) :
    now_date = datetime.datetime.now().strftime('%Y-%m-%d')  # 현재 날짜 받아옴

    sql = 'SELECT url FROM article_data WHERE category = "A1" AND publication_date = %s'
    cursor.execute(sql, [now_date])

    return [item[0] for item in cursor.fetchall()]  # DB 요청 반환값의 가장 첫번째 요소(URL) 반환

# DB에 데이터 저장시 중복저장을 회피하기 위해 마지막으로 저장된 {category = A2, publication_date = 현재날짜} 의 데이터의 URL 받아옴
def get_A2_urls(cursor) :
    now_date = datetime.datetime.now().strftime('%Y-%m-%d')   # 현재 날짜 받아옴

    sql = 'SELECT url FROM article_data WHERE category = "A2" AND publication_date = %s'
    cursor.execute(sql, [now_date])

    return [item[0] for item in cursor.fetchall()]  # DB 요청 반환값의 가장 첫번째 요소(URL) 반환

# DB에 데이터 저장시 중복저장을 회피하기 위해 마지막으로 저장된 {category = A3, publication_date = 현재날짜} 의 데이터의 URL 받아옴
def get_A3_urls(cursor) :
    now_date = datetime.datetime.now().strftime('%Y-%m-%d')   # 현재 날짜 받아옴

    sql = 'SELECT url FROM article_data WHERE category = "A3" AND publication_date = %s'
    cursor.execute(sql, [now_date])

    return [item[0] for item in cursor.fetchall()]  # DB 요청 반환값의 가장 첫번째 요소(URL) 반환