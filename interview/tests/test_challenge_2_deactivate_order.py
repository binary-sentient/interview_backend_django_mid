from django.http import HttpRequest
from django.test import TestCase
from rest_framework.test import APIRequestFactory

from interview.inventory.models import (
    Inventory,
    InventoryLanguage,
    InventoryTag,
    InventoryType,
)
from interview.order.models import Order
from interview.order.views import DeactivateOrderView


class Test_DeactivateOrderView(TestCase):
    def setUp(self):
        self.inventory_type = InventoryType.objects.create(
            name='Test Inventory Type'
        )
        self.inventory_language = InventoryLanguage.objects.create(
            name='Test Inventory Language'
        )
        self.inventory_tag = InventoryTag.objects.create(
            name='Test Inventory Tag'
        )
        self.inventory = Inventory.objects.create(
            name='Test Inventory',
            type=self.inventory_type,
            language=self.inventory_language,
            metadata={'test': 'metadata'}
        )
        self.inventory.tags.set([self.inventory_tag])
        self.order = Order.objects.create(
            inventory=self.inventory,
            embargo_date='2021-01-01',
            start_date='2021-01-01',
            is_active=True
        )
        self.view = DeactivateOrderView()
        self.request = HttpRequest()
        self.request.method = 'POST'
    
    def test_perform_update(self):
        factory = APIRequestFactory()
        request = factory.patch(f'/orders/{self.order.id}/deactivate/', {'id': self.order.id}, format='json')
        view = DeactivateOrderView.as_view()
        response = view(request, pk=self.order.id)
        self.order.refresh_from_db()
        self.assertFalse(self.order.is_active)
        self.assertEqual(response.status_code, 200)
