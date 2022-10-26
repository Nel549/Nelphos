from django.urls import path
from . import views

urlpatterns = [
    path('', views.presets, name='presets'),
    path('upload/', views.preset_add, name='preset-add'),
    path('<int:id>/', views.preset_detail, name='preset-detail'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('edit-preset/<int:id>', views.edit_preset, name='edit_preset'),
    path('add-to-cart', views.add_to_cart, name='add-to-cart'),
    path('<int:pk>/add-to-cart2', views.add_to_cart2, name='add_to_cart'),
    path('tag/<str:name>', views.tag, name='tag')
]   