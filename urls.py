from django.conf import settings
from django.conf.urls.defaults import *

urlpatterns = patterns('',
                       (r'^$', 'status.views.index'),
                       (r'^page/(?P<page>\d+)$', 'status.views.index'),
                       (r'^image/thumb/(?P<filename>.*)$', 'status.views.file',
                        {'collection_or_filename': 'thumb'}),
                       (r'^image/(?P<collection_or_filename>.*)$', 'status.views.file'),
                       (r'^static/(?P<path>.*)$', 'django.views.static.serve',
                        {'document_root': settings.STATIC_DOC_ROOT}),
                       )
