from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Products


@registry.register_document
class DocumentProduct(Document):
    class Index:
        name = 'main'
        search = {'number_of_shards': 1, 'number_of_replicas': 0}

    product_name = fields.TextField(
        attr='product_name',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        })
    product_type = fields.TextField(
        attr='product_type',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        })
    product_description = fields.TextField(
        attr='product_description',
        fields={
            'raw': fields.TextField(),
        })
    product_price = fields.IntegerField(
        attr='product_price',
        fields={
            'raw': fields.IntegerField(),
        })
    product_count = fields.IntegerField(
        attr='product_count',
        fields={
            'raw': fields.IntegerField(),
        })

    class Django:
        model = Products
