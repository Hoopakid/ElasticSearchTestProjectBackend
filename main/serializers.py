from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework import serializers

from main.documents import DocumentProduct
from main.models import Products


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
        read_only_fields = ('created_at',)


class ProductDocumentSerializer(DocumentSerializer):
    class Meta:
        document = DocumentProduct
        fields = ('product_name', 'product_type', 'product_count', 'product_price', 'product_description')
