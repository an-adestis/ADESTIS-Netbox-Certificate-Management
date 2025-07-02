from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'netbox_cars'

router = NetBoxRouter()
router.register('cars', views.CarsViewSet)

urlpatterns = router.urls
