from django.urls import include, path
from main import views

app_name = 'main'

urlpatterns = [
	path('ai/',views.ai, name='ai'),
	path('xml/', views.upload_csv, name='upload_csv'),
	# path("inner-page/", views.inner, name="inner"),
	path('image-resize/', views.image_resize,name='image_resize'),
	path('redirect-builder/', views.redirect_builder_view,name='redirect-builder')
	]