
from products import views

from django.conf.urls import url

from .views import (
    ProductListView,
    ProductDetailSlugView, 

    )


urlpatterns = [

    url(r'^$', ProductListView.as_view(), name='list'),
    url(r'^(?P<slug>[\wi-]+)/$', ProductDetailSlugView.as_view(), name='detail'),

]

