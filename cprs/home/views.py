from collections import Counter
from django.shortcuts import render
from django.views import View
from .models import *

class HomeView(View):
    template = 'home/index.html'

    def get(self, request):
        ctx = {
            'brands': Brand.objects.all(),
            'items': Item.objects.all()
        }
        return render(request, self.template, ctx)

class SignInView(View):
    template = 'home/sign-in.html'

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
