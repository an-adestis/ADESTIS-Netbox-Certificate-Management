from django import forms
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm, NetBoxModelBulkEditForm, NetBoxModelImportForm
from utilities.forms.fields import CommentField, CSVChoiceField, TagFilterField
from adestis_netbox_certificate_management.models.certificate import Certificate, CertificateStatusChoices
from django.utils.translation import gettext_lazy as _
from utilities.forms.rendering import FieldSet

__all__ = (
    'CertificateForm',
    'CertificateFilterForm',
    'CertificateBulkEditForm',
    'CertificateCSVForm',
)

class CertificateForm(NetBoxModelForm):
    comments = CommentField()


    fieldsets = (
        FieldSet('status', 'tags'),
    )

    class Meta:
        model = Certificate
        fields = ['status', 'comments', 'tags']
        help_texts = {
            'status': "Example text",
        }


class CertificateBulkEditForm(NetBoxModelBulkEditForm):
    pk = forms.ModelMultipleChoiceField(
        queryset=Certificate.objects.all(),
        widget=forms.MultipleHiddenInput
    )

    status = forms.ChoiceField(
        required=False,
        choices=CertificateStatusChoices,
    )

    model = Certificate

    fieldsets = (
        FieldSet('status'),
    )

    nullable_fields = [
         'add_tags', 'remove_tags'
    ]


class CertificateFilterForm(NetBoxModelFilterSetForm):
    
    model = Certificate

    fieldsets = (
        FieldSet('q', 'index', 'tag'),
        FieldSet('status'),
    )

    index = forms.IntegerField(
        required=False
    )

    status = forms.MultipleChoiceField(
        choices=CertificateStatusChoices,
        required=False,
        label=_('Status')
    )

    tag = TagFilterField(model)


class CertificateCSVForm(NetBoxModelImportForm):

    status = CSVChoiceField(
        choices=CertificateStatusChoices,
        help_text=_('Status'),
        required=True,
    )

    class Meta:
        model = Certificate
        fields = ['status']
        default_return_url = 'plugins:adestis_netbox_certificate_management:certificate_list'
