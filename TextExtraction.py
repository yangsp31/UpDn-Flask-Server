# 추출한 articleSummary 데이터를 DB에 저장하기 위한 형식으로 가공
def get_article_summary(summary_element) :
    for span in summary_element.find_all('span') :  # 추출한 데이터 내의 [span] 속성을 모두 제거한 형태의 데이터로 가공
        span.decompose()

    return summary_element.get_text(strip = True)   # 가공된 데이터의 text를 반환