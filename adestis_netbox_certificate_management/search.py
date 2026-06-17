from netbox.search import SearchIndex, register_search
from adestis_netbox_certificate_management.models import *

@register_search
class CertificateIndex(SearchIndex):
    model = Certificate
    fields = (
        ('name', 1000),
        ('description', 500),
        ('comments', 2000),
        ('subject', 500),
        ('issuer', 500),
        ('supplier_product', 500),
        ('authority_identifier', 1000),
        ('subject_key_identifier', 1000),
        ('subject_alternative_name', 1000),
        ('key_technology', 1000),
        ('status', 1000),
    )