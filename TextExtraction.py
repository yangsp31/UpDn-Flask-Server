def get_article_summary(summary_element) :
    for span in summary_element.find_all('span') :
        span.decompose()

    return summary_element.get_text(strip = True)