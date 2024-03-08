from django.db.models import Q
from .documents import DocumentProduct
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    SearchFilterBackend,
    SuggesterFilterBackend, DefaultOrderingFilterBackend, OrderingFilterBackend,
)
from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from main.models import Products
from main.serializers import ProductSerializer, ProductDocumentSerializer


class ProductAPIView(GenericAPIView):
    permission_classes = ()
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        product_serializer = ProductSerializer(data=request.data)
        product_serializer.is_valid(raise_exception=True)
        product_serializer.save()
        return Response(product_serializer.data)


class ProductUpdateAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Products.objects.all()

    def get(self, request, pk):
        try:
            product_instance = self.get_object()
            if product_instance:
                serializer = ProductSerializer(product_instance)
                return Response(serializer.data)
            else:
                return Response({'message': 'Product not found!'}, status=404)
        except Exception as e:
            return Response({'message': str(e)}, status=400)

    def put(self, request, pk):
        try:
            product_instance = self.get_object()
            if product_instance:
                serializer = self.serializer_class(instance=product_instance, data=request.data)
                if serializer.is_valid():
                    updated_product = serializer.save()
                    product_serializer = ProductSerializer(updated_product)
                    return Response(product_serializer.data)
                else:
                    return Response({'message': 'Product input invalid !'}, status=400)
            else:
                return Response({'message': 'Product not found!'}, status=404)
        except Exception as e:
            return Response({'message': str(e)}, status=400)


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ProductSearchViewSet(DocumentViewSet):
    document = DocumentProduct
    serializer_class = ProductDocumentSerializer
    pagination_class = CustomPageNumberPagination

    filter_backends = [
        FilteringFilterBackend,
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
        SuggesterFilterBackend,
    ]

    search_fields = (
        'product_name',
        'product_type',
        'product_description',
        'product_price',
        'product_count'
    )

    filter_fields = {
        'product_name': 'product_name',
        'product_type': 'product_type',
        'product_description': 'product_description',
        'product_price': 'product_price',
        'product_count': 'product_count'
    }

    suggester_fields = {
        'product_name': {
            'field': 'product_name.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
        'product_type': {
            'field': 'product_type.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        }
    }

    def list(self, request, *args, **kwargs):
        search_term = self.request.query_params.get('query', '')
        print(search_term)
        query = Q('multi_match', query=search_term, fields=self.search_fields)
        queryset = self.filter_queryset(self.get_queryset().query(query))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
