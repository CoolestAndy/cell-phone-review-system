import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)


class HomeConfig(AppConfig):
    name = 'home'
    item_searcher = None
    review_searcher = None

    def ready(self):
        from .models import Item, Review
        from .searcher import ItemSearcher, ReviewSearcher
        print("Initializing search engine...")
        try:
            self.item_searcher = ItemSearcher(Item.objects.all())
            self.review_searcher = ReviewSearcher(Review.objects.all())
            print("Initialization done.")
        except Exception as e:
            logger.error("Failed to initialize search engine.")
            logger.error(e)
