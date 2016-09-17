from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$',views.login),
    url(r'^logout/$',views.logout),
    url(r'^regist/$',views.regist),
    url(r'^index/$',views.IndexView.as_view(),name='index'),
    # name属性是在网页中的{% url 'index' article_id %}中的'index'
    url(r'^detail/(?P<article_id>\d+)$',views.Detail.as_view(),name='detail'),
    url(r'^comment/$',views.comment),
    url(r'^message/$',views.message),
    url(r'^test/$',views.test)
]