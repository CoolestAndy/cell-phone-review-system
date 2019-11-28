from collections import Counter
from django.shortcuts import render
from django.views import View
from .models import *

class HomeView(View):
    template = 'home/index.html'

    def get(self, request):
        brand_filter = request.GET.get("brand", "")
        rating_filter = request.GET.get("rating", 0)
        min_price_filter = request.GET.get("min_price", "")
        max_price_filter = request.GET.get("max_price", "")
        items = []
        for item in Item.objects.all():
            if brand_filter and item.brand.name != brand_filter:
                continue
            if rating_filter and item.average_rating < float(rating_filter):
                continue
            if min_price_filter and (item.max_price is None or item.max_price < float(min_price_filter)):
                continue
            if max_price_filter and (max_price_filter is None or item.min_price > float(max_price_filter)):
                continue
            items.append(item)
        ctx = {
            'brands': Brand.objects.all(),
            'items': items,
            'filters': {
                'brand': brand_filter,
                'rating': rating_filter,
                'min_price': min_price_filter,
                'max_price': max_price_filter
            }
        }
        return render(request, self.template, ctx)

class SignInView(View):
    template = 'home/login.html'

    def get(self, request):
        return render(request, self.template)

class DetailsView(View):
    template = 'home/details.html'

    def get(self, request, asin):
        item = Item.objects.get(asin=asin)
        reviews = Review.objects.filter(item=item)
        rating_count = Counter(item.ratings.all())
        rating_count = { rating.rating: count for rating, count in rating_count.items()}
        ctx = {
            'ratings': {
                'ticks': [0.5, 1.5, 2.5, 3.5, 4.5],
                'count': rating_count,
                'percentage': {
                    rating: '{}%'.format(count * 100 / max(rating_count.values()))
                    for rating, count in rating_count.items()
                }
            },
            'item': item,
            'reviews': reviews
        }
        return render(request, self.template, ctx)
