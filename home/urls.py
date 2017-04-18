from django.conf.urls import url
from . import views

app_name = 'home'

urlpatterns = [
    url(r'^json/$', views.PostListSerializer.as_view()),
    url(r'^json/(?P<pk>[0-9]+)/$', views.PostDetailSerializer.as_view()),

    url(r'^$', views.PostListView.as_view(), name='post_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'\
        r'(?P<post>[-\w]+)/(?P<pk>[0-9]+)/$', views.PostDetail.as_view(), name='post_detail'),

    url(r'^register/$', views.UserFormView.as_view(), name='register'),

    url(r'^post/add/$', views.PostCreate.as_view(), name='post_add'),

    url(r'^post/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/'\
        r'(?P<post>[-\w]+)/(?P<pk>[0-9]+)/up/$',
        views.PostUpdate.as_view(), name='post_update'),

    url(r'^(?P<pk>[0-9]+)/$', views.PostDelete.as_view(), name='post_delete'),

    url(r'^(?P<pk>\d+)/share/$', views.PostShare.as_view(), name='post_share'),

    url(r'^login/$', views.UserLogIn.as_view(), name='log_in'),

    url(r'^logout/$', views.UserLogout.as_view(), name='log_out'),
]