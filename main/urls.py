from django.urls import path, include
from . import views



app_name = "main"

urlpatterns = [
    path("", views.show_main, name="show_main"),
    path("product/<uuid:id>/", views.show_product, name="show_product"),
    path("product/<uuid:id>/delete/", views.delete_product, name="delete_product",),
	path("product/<uuid:id>/edit", views.edit_product, name='edit_product'),
	
    # flutter integration
	path('proxy-image/', views.proxy_image, name='proxy_image'),
	path('create-product-flutter/', views.create_product_flutter, name='create_product_flutter'),

	# Login/Registration functions
	path('register/', views.register, name='register'),
	path('login/', views.login_user, name='login'),
	path('logout/', views.logout_user, name='logout'),

    # XML/JSON paths
    path("xml/", views.show_xml, name="show_xml"),
    path("json/", views.show_json, name="show_json"),
    path("my-json/", views.show_my_json, name="show_my_json"),
    path("xml/<uuid:product_id>/", views.show_xml_by_id, name="show_xml_by_id"),
    path("json/<uuid:product_id>/", views.show_json_by_id, name="show_json_by_id"),
	
    # AJAX Implementation
	path('add_product_entry_ajax/', views.add_product_entry_ajax, name='add_product_entry_ajax')
]