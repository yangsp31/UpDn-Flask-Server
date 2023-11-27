import datetime

def get_A1_urls(cursor) :
    now_date = datetime.datetime.now().strftime('%Y-%m-%d')

    sql = 'SELECT url FROM article_data WHERE category = "A1" AND publication_date = %s'
    cursor.execute(sql, [now_date])

    return [item[0] for item in cursor.fetchall()]

def get_A2_urls(cursor) :
    now_date = datetime.datetime.now().strftime('%Y-%m-%d')

    sql = 'SELECT url FROM article_data WHERE category = "A2" AND publication_date = %s'
    cursor.execute(sql, [now_date])

    return [item[0] for item in cursor.fetchall()]

def get_A3_urls(cursor) :
    now_date = datetime.datetime.now().strftime('%Y-%m-%d')

    sql = 'SELECT url FROM article_data WHERE category = "A3" AND publication_date = %s'
    cursor.execute(sql, [now_date])

    return [item[0] for item in cursor.fetchall()]