from django.conf.urls import url
from pages import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
    # url(r'^$', views.HomePageView.my_view),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)