from django.urls import path
from netbox.views.generic import ObjectChangeLogView
from adestis_netbox_certificate_management.models import *
from adestis_netbox_certificate_management.views.certificate import *
from adestis_netbox_certificate_management.models import *
from django.urls import include
from utilities.urls import get_model_urls

urlpatterns = (

    # Certificates
    path('certificate/', CertificateListView.as_view(),
         name='certificate_list'),
    path('certificate/add/', CertificateEditView.as_view(),
         name='certificate_add'),
    path('certificate/delete/', CertificateBulkDeleteView.as_view(),
         name='certificate_bulk_delete'),
    path('certificate/edit/', CertificateBulkEditView.as_view(),
         name='certificate_bulk_edit'),
    path('certificate/import/', CertificateBulkImportView.as_view(),
         name='certificate_bulk_import'),
    path('certificates/import_certificate/', CertificateBulkImportCertificateView.as_view(),
         name='certificate_bulk_import_certificate'),
    path('certificates/successorcertificates/', CertificateAffectedSuccessorCertificateView.as_view(),
         name='successorcertificates_list'),
    path('certificates/prodecessorcertificates/', CertificateAffectedProdecessorCertificateView.as_view(),
         name='prodecessorcertificates_list'), 
    path('certificates/applications/', CertificateAffectedInstalledApplicationView.as_view(),
         name='certificateapplications_list'),
    path('certificates/devices/', DeviceAffectedCertificateView.as_view(),
         name='certificatedevices_list'),
    path('certificates/clusters/', ClusterAffectedCertificateView.as_view(),
         name='certificateclusters_list'),
    path('certificates/clustergroups/', ClusterGroupAffectedCertificateView.as_view(),
         name='certificateclustergroups_list'),
    path('certificates/virtualmachines/', VirtualMachineAffectedCertificateView.as_view(),
         name='certificatevirtualmachines_list'),
    path('certificates/contacts/', ContactAffectedCertificateView.as_view(),
         name='certificatecontacts_list'),
    path('certificates/devices/', CertificateAffectedDeviceView.as_view(),
         name='certificatedevices_list'),
    path('certificates/clusters/', CertificateAffectedClusterView.as_view(),
         name='certificateclusters_list'),
    path('certificates/clustergroups/', CertificateAffectedClusterGroupView.as_view(),
         name='certificateclustergroups_list'),
    path('certificates/virtualmachines/', CertificateAffectedVirtualMachineView.as_view(),
         name='certificatevirtualmachines_list'),
    path('certificates/contacts/', CertificateAffectedContactView.as_view(),
         name='certificatecontacts_list'),
    
    
    
    path('certificate/<int:pk>/',
         CertificateView.as_view(), name='certificate'),
    path('certificate/<int:pk>/',
         include(get_model_urls("adestis_netbox_certificate_management", "certificate"))),
    path('certificate/<int:pk>/edit/',
         CertificateEditView.as_view(), name='certificate_edit'),
    path('certificate/<int:pk>/delete/',
         CertificateDeleteView.as_view(), name='certificate_delete'),
    path('certificate/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='certificate_changelog', kwargs={
        'model': Certificate
    }),
    
    path('certificates/tenants/', TenantAffectedCertificateView.as_view(),
         name='certificatetenants_list'), 

)
