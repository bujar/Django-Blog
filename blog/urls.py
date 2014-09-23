from django.conf.urls import patterns, url

from blog import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    (r'^confirm/([_%&\-+0-9a-zA-Z ]+)/$', views.confirm),
    (r'^view_blog/([_%&\-+0-9a-zA-Z ]+)/$', views.view_blog),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'blog/login.html'}),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/blog/'}),
    url(r'^register$', 'blog.views.register'),
    url(r'^add-item', views.add_item),
    url(r'^delete-item/(?P<item_id>\d+)$', 'blog.views.delete_item'),
    url(r'^manage', views.manage),
    url(r'^photo/(?P<item_id>\d+)$', 'blog.views.photo', name='photo'),
    url(r'^getUserList$', 'blog.views.getUserList'),

)