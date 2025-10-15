from django.urls import path

from . import views

app_name = "hr"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('list/', views.PersonListView.as_view(), name='person_list'),
]