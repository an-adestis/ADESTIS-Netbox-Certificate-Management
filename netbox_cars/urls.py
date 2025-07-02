from django.urls import path
from netbox.views.generic import ObjectChangeLogView
from netbox_cars.models import *
from netbox_cars.views import *
from netbox_cars.views.cars import *
from netbox_cars.models import *
from django.urls import include
from utilities.urls import get_model_urls

urlpatterns = (

    # Applications
    path('cars/', CarsListView.as_view(),
         name='cars_list'),
    path('cars/add/', CarsEditView.as_view(),
         name='cars_add'),
    path('cars/delete/', CarsBulkDeleteView.as_view(),
         name='cars_bulk_delete'),
    path('cars/edit/', CarsBulkEditView.as_view(),
         name='cars_bulk_edit'),
    path('cars/import/', CarsBulkImportView.as_view(),
         name='cars_bulk_import'),
    path('cars/<int:pk>/',
         CarsView.as_view(), name='cars'),
    path('cars/<int:pk>/',
         include(get_model_urls("netbox_cars", "cars"))),
    path('cars/<int:pk>/edit/',
         CarsEditView.as_view(), name='cars_edit'),
    path('cars/<int:pk>/delete/',
         CarsDeleteView.as_view(), name='cars_delete'),
    path('cars/applications/', InstalledApplicationAffectedCarsView.as_view(),
         name='carsapplications_list'),
    path('cars/<int:pk>/changelog/', ObjectChangeLogView.as_view(), name='cars_changelog', kwargs={
        'model': Cars
    }),

)
