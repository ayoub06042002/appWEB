# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('performance/', views.performance_pivot, name='performance'),
    path('performance/<int:year>/<int:month>/', views.performance_daily, name='performance_daily'),
    path('performance/add/', views.add_performance, name='add_performance'),
    path('performance/daily/<int:year>/<int:month>/delete/<int:performance_id>/', views.delete_performance, name='delete_performance'),
    path('graph_performance/', views.graph_performance, name='graph_performance'),
    path('performance/<int:year>/<int:month>/edit/<int:performance_id>/', views.edit_performance, name='edit_performance'),
    
]
