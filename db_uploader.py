import os, django, csv, sys
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "madup.settings")
django.setup()

from ads.models import *
from advertisers.models import *

CSV_PATH_ADS_advertiser_info = './csv/Madup_Wanted_Data_set(deleted).csv'

with open(CSV_PATH_ADS_advertiser_info) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        advertiser_id = row[0]
        try:
            advertiser_info.objects.create(advertiser_id = advertiser_id)
        except:
            pass

CSV_PATH_ADS_ad_info = './csv/Madup_Wanted_Data_set(deleted).csv'

with open(CSV_PATH_ADS_ad_info) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        advertiser_id = row[0]
        uid = row[1]
        media = row[2]
        try:
            ad_info.objects.create(advertiser_id = advertiser_id, uid = uid, media = media)
        except:
            pass

CSV_PATH_ADS_result_data_set = './csv/Madup_Wanted_Data_set(deleted).csv'

with open(CSV_PATH_ADS_result_data_set) as in_file:
    data_reader = csv.reader(in_file)
    next(data_reader, None)
    for row in data_reader:
        advertiser_id = row[0]
        uid_id = row[1]
        media = row[2]
        ##date 포멧변경
        date = row[3]
        date_format = '%Y.%m.%d'
        date = datetime.strptime(date, date_format)
        date = date.date()
        ###
        cost = row[4]
        impression = row[5]
        click = row[6]
        conversion = row[7]
        cv = row[8]
        try:
            result_data_set.objects.create(advertiser_id = advertiser_id, uid_id = uid_id, media = media, date = date, 
            cost = cost, impression = impression, click = click, conversion = conversion, cv = cv)
        except:
            print("입력실패")
