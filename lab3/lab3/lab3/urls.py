from django.contrib import admin
from app import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path(r'word_card/', views.WordCardList.as_view(), name='wordcards-list'),
    path(r'word_card/<int:pk>/', views.WordCardDetail.as_view(), name='wordcards-detail'),
    path(r'word_card/<int:pk>/put/', views.put, name='wordcard-put'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]