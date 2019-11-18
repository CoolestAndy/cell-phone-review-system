import csv
import json
from datetime import datetime
from tqdm import tqdm

from home.models import *


def run():
    Manufacturer.objects.all().delete()
    Language.objects.all().delete()
    Rating.objects.all().delete()
    User.objects.all().delete()
    Country.objects.all().delete()
    Phone.objects.all().delete()
    Review.objects.all().delete()

    with open('data/phone_images.json', 'r', encoding='utf-8') as f:
        images = json.load(f)
    with open('data/phone_user_review_file.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in tqdm(reader, total=1415134):
            try:
                manufacturer, _ = Manufacturer.objects.all().get_or_create(name=row[4])
                language, _ = Language.objects.all().get_or_create(name=row[2])
                country, _ = Country.objects.all().get_or_create(name=row[3])
                rating, _ = Rating.objects.all().get_or_create(rating=5)
                image = images[row[0].split('/')[2]]
                author, _ = User.objects.all().get_or_create(username=row[9])
                phone, _ = Phone.objects.all().get_or_create(name=row[10], manufacturer=manufacturer, image=image)
                Review.objects.all().create(
                    content=row[8],
                    author=author,
                    time=datetime.strptime(row[1], '%m/%d/%Y'),
                    language=language,
                    country=country,
                    rating=rating,
                    phone=phone
                )
            except Exception as e:
                print("Failed to create object for", row)
                print(e)
