import os, django, csv, sys
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bear.settings")
django.setup()

from pos.models import *

CSV_PATH_POS_RESULT_DATA = './csv/bear_pos_example.csv'

with open(CSV_PATH_POS_RESULT_DATA) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        restaurant      = row[2]
        try:
            Restaurant.objects.create(id=restaurant)
        except:
            pass

with open(CSV_PATH_POS_RESULT_DATA) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        # id              = row[0] 자동 생성이므로 추가 X
        timestamp       = row[1]
        date_format = '%Y-%m-%d %H:%M:%S'
        timestamp = datetime.strptime(timestamp, date_format)
        restaurant      = row[2]
        price           = row[3]
        number_of_party = row[4]
        payment         = row[5]
        
        PosResultData.objects.create(timestamp=timestamp, restaurant_id=restaurant, price=price, number_of_party=number_of_party, payment=payment)

