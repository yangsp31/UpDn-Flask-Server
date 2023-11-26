import datetime

def get_M1_market_urls(cursor) :
    now_date = datetime.datetime.now().strftime('%Y-%m-%d')

    sql = 'SELECT url FROM market_article WHERE category = "M1" AND publication_date = %s'
    cursor.execute(sql, [now_date])

    return [item[0] for item in cursor.fetchall()]

def get_M2_market_urls(cursor) :
    now_date = datetime.datetime.now().strftime('%Y-%m-%d')

    sql = 'SELECT url FROM market_article WHERE category = "M2" AND publication_date = %s'
    cursor.execute(sql, [now_date])

    return [item[0] for item in cursor.fetchall()]

def get_company_urls(cursor) :
    now_date = datetime.datetime.now().strftime('%Y-%m-%d')

    sql = 'SELECT url FROM company_article WHERE publication_date = %s'
    cursor.execute(sql, [now_date])

    return [item[0] for item in cursor.fetchall()]