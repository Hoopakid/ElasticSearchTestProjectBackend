from django.urls import path, include
from rest_framework import routers

from main.views import ProductAPIView, ProductUpdateAPIView, ProductSearchViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register('product-search', ProductSearchViewSet, basename='search_product')

urlpatterns = [
    path('product/', ProductAPIView.as_view(), name='Crud of Product'),
    path('product-detail/<int:pk>', ProductUpdateAPIView.as_view(), name='Get Product by id'),
    path('', include(router.urls)),
]
