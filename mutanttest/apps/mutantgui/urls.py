from django.conf.urls import patterns, url


urlpatterns = patterns('mutantgui.views',
    url(r'^tables/$', 'list_tables', name='table_list'),
    url(r'^tables/create/$', 'create_table', name='table_create'),
    url(r'^tables/(?P<pk>\d+)/update/$', 'update_table', name='table_update'),
    url(r'^tables/(?P<pk>\d+)/delete/$', 'delete_table', name='table_delete'),

    url(r'^tables/(?P<table_pk>\d+)/fields/$', 'list_fields', name='field_list'),
    url(r'^tables/(?P<table_pk>\d+)/fields/create/$', 'create_field', name='field_create'),
    url(r'^tables/(?P<table_pk>\d+)/fields/(?P<field_pk>\d+)/update/$', 'update_field', name='field_update'),
    url(r'^tables/(?P<table_pk>\d+)/fields/(?P<pk>\d+)/delete/$', 'delete_field', name='field_delete'),
)
