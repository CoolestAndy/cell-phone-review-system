from queue import PriorityQueue
from django.db import models
from .ranker import Ranker
from .models import Item, Review

class Searcher:
    def __init__(self, objects: [models.Model], adaptor, **kwargs):
        self.maxsize = 0
        self.adaptor = adaptor
        self.ranker = Ranker(**kwargs)
        self.ranker.make_inverted_index([adaptor(obj) for obj in objects], [obj.pk for obj in objects])

    def add_object(self, obj: models.Model):
        self.ranker.add_document(self.adaptor(obj), obj.pk)

    def remove_object(self, obj: models.Model):
        self.ranker.remove_document(self.adaptor(obj), obj.pk)

    def search(self, objects: [models.Model], query: str) -> [models.Model]:
        heap = PriorityQueue(maxsize=self.maxsize)
        for obj in objects:
            if heap.full():
                heap.get()
            heap.put((self.ranker.score(obj.pk, query), obj.pk, obj))
        return [obj for score, _, obj in sorted(heap.queue, reverse=True) if score > 0]


class ItemSearcher(Searcher):
    def __init__(self, items: [Item], **kwargs):
        adaptor = lambda item: item.title
        super().__init__(items, adaptor, **kwargs)


class ReviewSearcher(Searcher):
    def __init__(self, reviews: [Review], **kwargs):
        adaptor = lambda review: review.title + ' ' + review.body
        super().__init__(reviews, adaptor, **kwargs)
