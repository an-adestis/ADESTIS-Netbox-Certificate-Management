from netbox.views import generic
from netbox_certificate_management.forms import *
from netbox_certificate_management.models import *
# from netbox_certificate_management.filtersets import CertificateFilterSet
from netbox_certificate_management.tables import *
from netbox.views import generic
from django.utils.translation import gettext as _
from netbox_certificate_management.models import *
from netbox_certificate_management.tables import *
from adestis_netbox_applications.models import InstalledApplication
from adestis_netbox_applications.tables import InstalledApplicationTable
from utilities.views import GetRelatedModelsMixin, ViewTab, register_model_view
from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import ValidationError
import cert_utils 
import hashlib
from django.urls import reverse
from django.db import transaction
from django.contrib import messages
import re


__all__ = (
    'CertificateView',
    'CertificateListView',
    'CertificateEditView',
    'CertificateDeleteView',
    'CertificateBulkDeleteView',
    'CertificateBulkEditView',
    'CertificateBulkImportView',
    'InstalledApplicationAffectedCertificateView',
    'CertificateAffectedInstalledApplicationView',
    'CertificateAssignApplication',
    'CertificateBulkImportCertificateView',
    'CertificateRemoveApplicationView',
)

class CertificateView(generic.ObjectView):
    queryset = Certificate.objects.all()

class CertificateListView(generic.ObjectListView):
    queryset = Certificate.objects.all()
    table = CertificateTable
    # filterset = CertificateFilterSet
    filterset_form = CertificateFilterForm
    template_name = 'netbox_certificate_management/cert_import.html'
    

class CertificateEditView(generic.ObjectEditView):
    queryset = Certificate.objects.all()
    form = CertificateForm


class CertificateDeleteView(generic.ObjectDeleteView):
    queryset = Certificate.objects.all() 

class CertificateBulkDeleteView(generic.BulkDeleteView):
    queryset = Certificate.objects.all()
    table = CertificateTable
    
    
class CertificateBulkEditView(generic.BulkEditView):
    queryset = Certificate.objects.all()
    # filterset = CertificateFilterSet
    table = CertificateTable
    form =  CertificateBulkEditForm
    

class CertificateBulkImportView(generic.BulkImportView):
    queryset = Certificate.objects.all()
    model_form = CertificateCSVForm
    table = CertificateTable
    
class CertificateBulkImportCertificateView(generic.ObjectEditView):
    queryset = Certificate.objects.all()
    template_name = 'netbox_certificate_management/crt_import.html'
    
    def get(self, request):
        form = CertificateCRTForm()
        context = {
            'form': form,
            'object': Certificate(),  # wichtig für object_edit.html
            'return_url': reverse('plugins:netbox_certificate_management:certificate_list'),
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = CertificateCRTForm(request.POST, request.FILES)
        if form.is_valid():
            files = request.FILES.getlist('certificate')
            created = []
            for file in files:
                        cert_text = file.read().decode()
                        
                        match = re.findall(r"-----BEGIN CERTIFICATE-----.*?-----END CERTIFICATE-----", cert_text, flags=re.DOTALL) # mit re.DOTALL werden Zeilenumbrüche (\n) mit eingebunden
                        if not match:
                             raise ValidationError("No valid certificate found in file")

                        for idx, single_cert in enumerate(match):
                            cleaned_cert = single_cert.replace("\r\n", "").replace("\n", "").strip()
                            
                            existing_cert = Certificate.objects.filter(certificate=cleaned_cert)
                            if existing_cert.exists():
                                existing_cert = existing_cert.first()
                                return redirect(existing_cert.get_absolute_url())
                            
                            cert_data = cert_utils.parse_cert(cert_text)
                            
                            subject_key_identifier = cert_data.get("subject_key_identifier")
                            if not subject_key_identifier:
                             subject_key_identifier = hashlib.sha1(cleaned_cert.encode()).hexdigest()
                            
                            common_name = cert_data["subject"]
                            for name,value in [ (pair.split("=")) for pair in cert_data["subject"].split("\n") ]:
                                if name == "CN":
                                    common_name=value
                                    
                            cert = Certificate.objects.create(
                                certificate=cleaned_cert,
                                name=common_name,
                                subject_key_identifier=subject_key_identifier
                            )
                        created.append(cert) #The append() method appends an element to the end of the list.
            if created:
                    return redirect(reverse('plugins:netbox_certificate_management:certificate_list'))
        context = {
            'form': form,
            'return_url': reverse('plugins:netbox_certificate_management:certificate_list'),
        }
        return render(request, self.template_name, context)        
        
    
@register_model_view(InstalledApplication, name='certificate')
class InstalledApplicationAffectedCertificateView(generic.ObjectChildrenView):
    queryset = InstalledApplication.objects.all()
    child_model= Certificate
    table = CertificateTable
    template_name = "netbox_certificate_management/certificate_application.html"
    actions = {
        'add': {'add'},
        'export': {'view'},
        'bulk_import': {'add'},
        'bulk_edit': {'change'},
        'bulk_remove_certificate': {'change'},
    }

    tab = ViewTab(
        label=_('Certificate'),
        # badge=lambda obj: obj.certificate.count(),
        hide_if_empty=False
    )

    def get_children(self, request, parent):
        return Certificate.objects.restrict(request.user, 'view').filter(installedapplication=parent)
    
@register_model_view(Certificate, name='applications')
class CertificateAffectedInstalledApplicationView(generic.ObjectChildrenView):
    queryset = Certificate.objects.all()
    child_model= InstalledApplication
    table = InstalledApplicationTable
    template_name = "netbox_certificate_management/application.html"
    actions = {
        'add': {'add'},
        'export': {'view'},
        'bulk_import': {'add'},
        'bulk_edit': {'change'},
        'bulk_remove_application': {'change'},
    }

    tab = ViewTab(
        label=_('Applications'),
        badge=lambda obj: obj.installedapplication.count(),
        weight=600
    )

    def get_children(self, request, parent):
        return InstalledApplication.objects.restrict(request.user, 'view').filter(installedapplication=parent)
    
@register_model_view(Certificate, 'assign_application')
class CertificateAssignApplication(generic.ObjectEditView):
    queryset = Certificate.objects.prefetch_related(
        'installedapplication', 'tags', 
    ).all()
    
    form = CertificateAssignApplicationForm
    template_name = 'netbox_certificate_management/assign_application.html'

    def get(self, request, pk):
        certificate = get_object_or_404(self.queryset, pk=pk)
        form = self.form(certificate,  initial=request.GET)

        return render(request, self.template_name, {
            'certificate': certificate,
            'form': form,
            'return_url': reverse('plugins:netbox_certificate_management:certificate', kwargs={'pk': pk}),
            'edit_url': reverse('plugins:netbox_certificate_management:certificate_assign_application', kwargs={'pk': pk}),
        })

    def post(self, request, pk):
        certificate = get_object_or_404(self.queryset, pk=pk)
        form = self.form(certificate, request.POST)

        if form.is_valid():
            
            selected_applications = form.cleaned_data['installedapplication']
            with transaction.atomic():
                
                for installedapplication in InstalledApplication.objects.filter(pk__in=selected_applications): 
                    certificate.installedapplication.add(installedapplication)
            
            certificate.save()
            
            return redirect(certificate.get_absolute_url())

        return render(request, self.template_name, {
            'certificate': certificate,
            'form': form,
            'return_url': certificate.get_absolute_url(),
            'edit_url': reverse('plugins:netbox_certificate_management:certificate_assign_application', kwargs={'pk': pk}),
        })
    
@register_model_view(Certificate, 'remove_application', path='application/remove')
class CertificateRemoveApplicationView(generic.ObjectEditView):
    queryset = Certificate.objects.all()
    form = CertificateRemoveApplication
    template_name = 'generic/bulk_remove.html'

    def post(self, request, pk):

        certificate = get_object_or_404(self.queryset, pk=pk)

        if '_confirm' in request.POST:
            
            form = self.form(request.POST)
            if form.is_valid():
                
                application_pks = form.cleaned_data['pk']
                with transaction.atomic():
                    certificate.installedapplication.remove(*application_pks)
                    certificate.save()

                messages.success(request, _("Removed {count} applications from certificate {certificate}").format(
                    count=len(application_pks),
                    certificate=certificate
                ))
                return redirect(certificate.get_absolute_url())
        else:
            form = self.form(initial={'pk': request.POST.getlist('pk')})

        selected_objects = InstalledApplication.objects.filter(pk__in=form.initial['pk'])
        application_table = InstalledApplicationTable(list(selected_objects), orderable=False)
        application_table.configure(request)

        return render(request, self.template_name, {
            'form': form,
            'parent_obj': certificate,
            'table': application_table,
            'obj_type_plural': 'applications',
            'return_url': certificate.get_absolute_url(),
        })  
    