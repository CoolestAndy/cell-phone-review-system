from django.apps import AppConfig


class HomeConfig(AppConfig):
    name = 'home'
    item_searcher = None
    review_searcher = None

    def ready(self):
        from .models import Item, Review
        from .searcher import ItemSearcher, ReviewSearcher
        print("Initializing search engine...")
        self.item_searcher = ItemSearcher(Item.objects.all())
        self.review_searcher = ReviewSearcher(Review.objects.all())
        print("Initialization done.")
