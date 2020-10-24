from .models import PriceOfTicket
from django.db import transaction
import requests
import traceback
from datetime import datetime, timedelta


class ParserData:

    def __init__(self):
        self.headers = {
            'Content-Type': 'application/json'
        }
        self.respons = []
        self.data_by_date = {}

    def start_parse(self, url):
        responce = self.get_data(url)
        self.sort_by_date(responce)
        self.parse_data()

    def check_url(self, dict_check):
        response = self.get_data(dict_check["url"])
        self.cheking_data(response, dict_check["id"])

    def cheking_data(self, data, id):
        obj = PriceOfTicket.objects.get(pk=id)
        obj.flights_checked = data.get('flights_checked')
        obj.flights_invalid = data.get('flights_invalid')
        obj.price_change = data.get('price_change')
        obj.save()

    def get_data(self, url):
        try:
            response = requests.get(url=url, headers=self.headers)
            if response.status_code == 404:
                return
            if response.status_code != 200:
                raise ValueError('Request to {} responded with status {}'.format(url, response.status_code))
            else:
                return response.json()
        except Exception:
            raise Exception('Error in getting html\n' + str(traceback.format_exc()))

    def sort_by_date(self, response):
        data = response['data']
        for i in data:
            date = str(datetime.utcfromtimestamp(i['dTime']).strftime('%Y-%m-%d'))  # .strftime('%Y-%m-%d %H:%M:%S')
            if date in self.data_by_date:
                self.data_by_date[date].append(i)
            else:
                self.data_by_date[date] = []
                self.data_by_date[date].append(i)

    def parse_data(self):
        for k, v in self.data_by_date.items():
            seq_price = [x['price'] for x in v]
            min_price = min(seq_price)
            v = [x for x in v if x['price'] == min_price]
            rows_for_ins = []
            with transaction.atomic():
                for i in v:
                    PriceOfTicket.objects.filter(id_in_api=i["id"]).delete()
                    pot = PriceOfTicket(id_in_api=i["id"],
                                      date=k,
                                      city_from=i["cityFrom"],
                                      city_to=i["cityTo"],
                                      price=i["price"],
                                      booking_token=i["booking_token"])
                    rows_for_ins.append(pot)

                PriceOfTicket.objects.bulk_create(rows_for_ins)


def create_urls():
    from_to = [
        {'from': "ALA", "to": "TSE"},
        {'from': "TSE", "to": "ALA"},
        {'from': "ALA", "to": "MOW"},
        {'from': "MOW", "to": "ALA"},
        {'from': "ALA", "to": "CIT"},
        {'from': "CIT", "to": "ALA"},
        {'from': "TSE", "to": "MOW"},
        {'from': "MOW", "to": "TSE"},
        {'from': "TSE", "to": "LED"},
        {'from': "LED", "to": "RSE"},
    ]
    date_now = datetime.now().strftime("%d/%m/%Y")
    now_30 = (datetime.now() + timedelta(30)).strftime("%d/%m/%Y")
    urls = [
        f'https://api.skypicker.com/flights?fly_from={i["from"]}&fly_to={i["to"]}&date_from={date_now}&date_to={now_30}&partner=picky'
        for i in from_to]
    return urls


def check_urls():
    urls = []
    objs = PriceOfTicket.objects.all()
    for i in objs:
        url = f'https://booking-api.skypicker.com/api/v0.1/check_flights?v=2&booking_token={i.booking_token}' \
              '&bnum=1' \
              '&pnum=1' \
              '&affily=picky_{market}' \
              '&currency=EUR&' \
              'adults=1' \
              '&children=0' \
              '&infants=0'
        urls.append({"url": url, "id": i.id})
    return urls
