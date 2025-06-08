from django.urls import path
from . import views
from .views import cancel_booking
from django.views.generic import RedirectView
from django.contrib import admin
from .views import user_login
from .views import profile_management
from .views import user_register
from .views import change_password

urlpatterns = [
    path("equipmentManagement/", views.equipmentManagement, name="equipmentManagement"),

    path("updateItem/<str:id>", views.updateItem, name="updateItem"),
    path("createItem/", views.createItem, name="createItem"),
    path("deleteItem/<str:id>/", views.deleteItem, name="deleteItem"),
  path("equipmentView/", views.equipmentView, name = "equipmentView"),
  path('book_item/<int:item_id>/', views.book_item, name='book_item'),
  path('bookings/', views.bookings_view, name='bookings_view'),
      path('historical/', views.historical, name='historical'),
    path('rebook/<int:item_id>/', views.rebook, name='rebook'),
     path('cancel_booking/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    path("bookings/<int:booking_id>/update/", views.booking_update, name="booking_update"),
    path("bookings/<int:booking_id>/delete/", views.booking_delete, name="deleteBooking"),
    path("bookings/create/", views.booking_create, name="createBooking"),
    path('userManagement/', views.user_management, name='user_management'),
    path('update_user/<int:pk>/', views.update_user, name='update_user'),
    path('delete_user/<int:pk>/', views.delete_user, name='delete_user'),
    path("reports/", views.reports, name="reports"),
    path('bookingManagement/', views.booking_management, name='booking_management'),
    path('add_user/', views.add_user, name='add_user'),
   
    path('reports/<int:item_id>/current_inventory_status/', views.current_inventory_status, name='current_inventory_status'),
    path('reports/<int:item_id>/equipment_usage_history/', views.equipment_usage_history, name='equipment_usage_history'),
    path('reports/<int:item_id>/warranty_report/', views.warranty_report, name='warranty_report'),
    path('reports/<int:item_id>/overdue_equipment/', views.overdue_equipment, name='overdue_equipment'),

    path('reports/all_current_inventory_status/', views.all_current_inventory_status, name='all_current_inventory_status'),

    path('admin/', admin.site.urls),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('profile/', views.profile_management, name='profile_management'),
    path('change-password/', views.change_password, name='change_password'),
    path('', RedirectView.as_view(url='/login/', permanent=True)),  
]

