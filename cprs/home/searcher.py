from queue import PriorityQueue
from .ranker import Ranker
from .models import Item, Review

class Searcher:
    def __init__(self, objects: [], maxsize=0, **kwargs):
        self.objects = objects
        self.maxsize = maxsize
        self.ranker = Ranker(**kwargs)

    def search(self, query: str) -> ([object], [float]):
        heap = PriorityQueue(maxsize=self.maxsize)
        for i, obj in enumerate(self.objects):
            if heap.full():
                heap.get()
            heap.put((self.ranker.score(i, query), i, obj))
        return [obj for score, _, obj in sorted(heap.queue, reverse=True) if score > 0]


class ItemSearcher(Searcher):
    def __init__(self, items: [Item], **kwargs):
        super().__init__(items, **kwargs)
        self.ranker.make_inverted_index([item.title for item in items])


class ReviewSearcher(Searcher):
    def __init__(self, reviews: [Review], **kwargs):
        super().__init__(reviews, **kwargs)
        self.ranker.make_inverted_index([review.title + ' ' + review.body for review in reviews])
