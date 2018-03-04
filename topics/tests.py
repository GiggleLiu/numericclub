from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import Topic


class TopicModelTests(TestCase):
    def test_order(self):
        pass

class TopicViewTests(TestCase):
    # test a view
    def test_list(self):
        response = self.client.get('/topics/list/')
        assert(response.status_code==200)
