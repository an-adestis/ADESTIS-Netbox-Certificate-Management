from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'adestis_netbox_certificate_management'

router = NetBoxRouter()
router.register('certificate', views.CertificateViewSet)

urlpatterns = router.urls
