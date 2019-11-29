from collections import Counter
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .models import *


class HomeView(View):
    template = 'home/index.html'

    def search_keywords(self, document, query):
        document = document.lower()
        for keyword in query.split(' '):
            if keyword.lower() not in document:
                return False
        return True

    def filter_items(self, items, filters):
        filtered_items = []
        for item in items:
            if filters['keywords'] and not self.search_keywords(item.title, filters['keywords']):
                continue
            if filters['brand'] and item.brand.name != filters['brand']:
                continue
            if filters['carrier'] and item.carrier.name != filters['carrier']:
                continue
            if filters['min_price'] and (item.max_price is None or item.max_price < float(filters['min_price'])):
                continue
            if filters['max_price'] and (item.min_price is None or item.min_price > float(filters['max_price'])):
                continue
            filtered_items.append(item)
        return filtered_items

    def sort_items(self, items, sort_key, order):
        if sort_key == 'name':
            items.sort(key=lambda item: item.title.lower(), reverse=order=='descending')
        elif sort_key == 'reviewers':
            items.sort(key=lambda item: item.total_reviews, reverse=order == 'descending')
        elif sort_key == 'rating':
            items.sort(key=lambda item: item.average_rating, reverse=order == 'descending')
        elif sort_key == 'price' and order == 'ascending':
            items.sort(key=lambda item: item.min_price if item.min_price else 0xffffff)
        elif sort_key == 'price' and order == 'descending':
            items.sort(key=lambda item: item.max_price if item.max_price else 0, reverse=True)

    def get(self, request):
        # filter
        filters = {
            'keywords': request.GET.get("keywords", ""),
            'brand': request.GET.get("brand", ""),
            'carrier': request.GET.get("carrier", ""),
            'min_price': request.GET.get("min_price", ""),
            'max_price': request.GET.get("max_price", "")
        }
        items = self.filter_items(Item.objects.all(), filters)

        # sort
        sort = request.GET.get("sort", "")
        sort_key, order = sort.split('-') if '-' in sort else ('', '')
        self.sort_items(items, sort_key, order)

        ctx = {
            'brands': Brand.objects.all(),
            'carriers': Carrier.objects.all(),
            'items': items,
            'filters': filters,
            'sort': sort
        }
        return render(request, self.template, ctx)


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


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, asin):
        comment = Review(
            item=Item.objects.get(asin=asin),
            author=self.request.user,
            rating=Rating.objects.get_or_create(rating=int(request.POST.get('rating')))[0],
            title=request.POST.get('title'),
            body=request.POST.get('body'),
            date=datetime.now(),
            helpful_votes=0
        )
        comment.save()
        return redirect(reverse('home:details', args=[asin]))


class CommentDeleteView(LoginRequiredMixin, View):
    def post(self, request, asin):
        reviews = Review.objects.filter(id=request.POST.get('review_id'))
        for review in reviews:
            if self.request.user == review.author:
                review.delete()
        return redirect(reverse('home:details', args=[asin]))
