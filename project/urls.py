"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from scorecard import api_viewsets
from scorecard import views


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'businessunits', api_viewsets.BusinessUnitViewSet)
router.register(r'businessunitgroups', api_viewsets.BusinessUnitGroupViewSet)
router.register(r'buscores', api_viewsets.BUScoreViewSet)
router.register(r'persons', api_viewsets.PersonViewSet)
router.register(r'products', api_viewsets.ProductViewSet)
router.register(r'productscores', api_viewsets.ProductScoreViewSet)
router.register(r'productsecuritycapabilities', api_viewsets.ProductSecurityCapabilityViewSet)
router.register(r'productsecurityroles', api_viewsets.ProductSecurityRoleViewSet)
router.register(r'securitycapabilities', api_viewsets.SecurityCapabilityViewSet)
router.register(r'securitycategories', api_viewsets.SecurityCategoryViewSet)
router.register(r'securityroles', api_viewsets.SecurityRoleViewSet)
router.register(r'securitysubcategories', api_viewsets.SecuritySubCategoryViewSet)
router.register(r'statuses', api_viewsets.StatusViewSet)

schema_view = get_swagger_view(title="Scorecard API")

urlpatterns = [
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.businessunitsview),
    url(r'^admin/', admin.site.urls),
    url(r'^api/syncproductpages', views.SyncProductPages.as_view()),
    url(r'^api/calculateallproductscores', views.CalculateAllProductScores.as_view()),
    url(r'^api/calculateproductscores', views.CalculateProductScores.as_view()),
    url(r'^api/updateproductcapabilities', views.UpdateProductCapabilities.as_view()),
    url(r'^businessunitsview', views.businessunitsview),
    url(r'^docs/', schema_view),
    url(r'^health', views.health),
    url(r'^proddetailsview', views.proddetailsview),
    url(r'^productsview', views.productsview),
    url(r'^submit', views.submit),

    # Wire up our API using automatic URL routing.
    # Additionally, we include login URLs for the browsable API.

    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
