import csv
import json
from datetime import datetime
from tqdm import tqdm

from home.models import *


def run():
    Brand.objects.all().delete()
    Rating.objects.all().delete()
    Carrier.objects.all().delete()
    User.objects.all().delete()
    Item.objects.all().delete()
    Review.objects.all().delete()

    with open('data/items.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in tqdm(reader, total=792):
            brand, _ = Brand.objects.get_or_create(name=row[1])
            carriers = [carrier for carrier in Carrier.CANDIDATES if carrier.replace('-', '').lower() in row[2].replace('-', '').lower()]
            carrier, _ = Carrier.objects.get_or_create(name=carriers[0] if carriers else 'Unlocked')
            prices = [float(price.replace('$', '')) for price in row[8].split(',') if price]
            Item.objects.create(
                asin=row[0],
                brand=brand,
                carrier=carrier,
                title=row[2],
                image=row[4],
                average_rating=row[5],
                total_reviews=row[7],
                min_price=min(prices) if prices else None,
                max_price=max(prices) if prices else None
            )

    with open('data/reviews.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in tqdm(reader, total=82794):
            item = Item.objects.get(asin=row[0])
            author, _ = User.objects.get_or_create(username=row[1])
            rating, _ = Rating.objects.get_or_create(rating=int(row[2]))
            Review.objects.create(
                item=item,
                author=author,
                rating=rating,
                date=datetime.strptime(row[3], '%B %d, %Y'),
                title=row[5],
                body=row[6],
                helpful_votes=int(row[7]) if row[7] else 0
            )
