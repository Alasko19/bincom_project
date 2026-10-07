from django.urls import path
from . import views

urlpatterns = [
    path('', views.level_1_pu_results, name='level_1'),
    path('lga-results/', views.question_2_lga_results, name='level_2'),
    path('add-polling-unit/', views.question_3_add_pu, name='level_3'),
    path('get-wards/', views.get_wards_by_lga, name='get_wards'),  # AJAX URL for Chained Combo Box
]