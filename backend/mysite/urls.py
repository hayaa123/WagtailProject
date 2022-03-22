from django.conf import settings
from django.urls import include, path 
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.contrib.sitemaps.views import sitemap

from search import views as search_views

from .api import api_router

import debug_toolbar

urlpatterns = [
    path('django-admin/', admin.site.urls),

    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),

    path('api/v2/', api_router.urls),
    # to filter a specific type of pages we use api/v2/pages/?type=Blog.blogPaage (eg)
    # to access specific field of a database we use api/v2/pages/1/?fields=_,banner_title,banner_cta ...etc
    # to access all the field except some field we use api/v2/pages/1/?fields=*,-banner_title,-banner_cta
    # for pagination we use api/v2/pages/?limit=4 (this gives us the first 4) 
    # for pagination we use api/v2/pages/?limit=4&offset=4 (this gives us the last 4)
    # to order the response by some field we use  api/v2/pages/?order=title
    # to order the response by some field in reverse we use  api/v2/pages/?order=-title
    # to search in a searchable fiels we use api/v2/pages/?search=blog 
    # to find a page by its html path http://127.0.0.1:8000/api/v2/pages/find/?html_path=/
    # 

    
    path('search/', search_views.search, name='search'),
    path('sitemap.xml', sitemap),

]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls)), ]

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
