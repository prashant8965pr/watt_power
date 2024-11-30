from django.urls import path

from .views import EnergyConsumerAPIview, SpeedCreateAPIview, dummy_template_view

urlpatterns = [
    path('speedCreate/', SpeedCreateAPIview.as_view()),
    path('energyGet/', EnergyConsumerAPIview.as_view()),
    path("dummy/", dummy_template_view, name="dummy_template"),
]
