from django.test import TestCase
from django.utils.http import urlencode
from interview.inventory.models import Inventory
from datetime import datetime, timedelta
from django.utils.dateparse import parse_datetime
from interview.inventory import views
from rest_framework.response import Response

class TestInventoryViews(TestCase):
    fixtures = ['inventory_views_fixtures.json']
    inventory_objs = Inventory.objects.all().order_by('created_at')

    @classmethod
    def setUpClass(cls):
        '''
        Clear all Inventory objects before running tests
        so that only those provided in fixtures are present in database
        '''
        all_inventory = Inventory.objects.all()
        all_inventory.delete()
        super(TestInventoryViews, cls).setUpClass()

    def request_inventory_after_date(self, after_date: str) -> Response:
        '''
        make a request to inventory endpoint with the provided date
        value as ?after_date= in query string
        '''
        after_date_query = urlencode({'after-date': after_date})
        path = f"/inventory/?{after_date_query}"
        return self.client.get(path)

    def test_inventory_list_view_with_invalid_after_date(self) -> None:
        '''
        Test that 400 status response is provided when an invalid date string 
        format is used
        '''
        response = self.request_inventory_after_date('invalid-date')
        self.assertIs(response.resolver_match.func.__name__, views.InventoryListCreateView.as_view().__name__)
        self.assertEquals(response.status_code, 400)

    def test_inventory_list_view_with_earliest_after_date(self) -> None:
        '''
        Test that Inventory list request with an after-date query string returns
        all inventory created after the date provided
        '''
        earliest_created_date = self.inventory_objs[0].created_at
        after_date = earliest_created_date - timedelta(1)
        response = self.request_inventory_after_date(after_date)
        self.assertEquals(response.status_code, 200)
        self.assertIs(response.resolver_match.func.__name__, views.InventoryListCreateView.as_view().__name__)
        self.assertEquals(len(response.data), len(self.inventory_objs))
        
        # verify each item in response data was created before the after_date provided
        for e in response.data:
            self.assertGreater(self.inventory_objs.get(id=e['id']).created_at, after_date)
            
    def test_inventory_list_view_with_latest_after_date(self) -> None:
        '''
        Test that inventory list request with an after-date query string beyond
        any existing records returns no data
        '''
        latest_created_date = self.inventory_objs.last().created_at
        response = self.request_inventory_after_date(latest_created_date)
        self.assertEquals(response.status_code, 200)
        self.assertIs(response.resolver_match.func.__name__, views.InventoryListCreateView.as_view().__name__)
        self.assertEquals(len(response.data), 0)
