from django.urls import path
from . import views

urlpatterns = [
    path('', views.level_1_pu_results, name='level_1'),
    path('lga-results/', views.level_2_lga_results, name='level_2'),
    path('add-polling-unit/', views.level_3_add_pu, name='level_3'),
]