from api_test.celery import app
from .utils import ParserData, create_urls, check_urls
import traceback


@app.task
def parse_task():
    parser = ParserData()
    for url in create_urls():
        try:
            parser.start_parse(url)
        except:
            print(traceback.format_exc())
    return 'done'

@app.task
def checking_task():
    parser = ParserData()
    for dict_check in check_urls():
        try:
            parser.check_url(dict_check)
        except:
            print(traceback.format_exc())
    return 'checked'
