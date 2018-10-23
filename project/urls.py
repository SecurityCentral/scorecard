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
from django_filters import rest_framework
from rest_framework import routers, serializers, viewsets, filters
from scorecard.views import businessunitsview, proddetailsview, health, productsview, submit
from scorecard.models import Product, ProductSecurityCapability, SecurityCapability, SecurityCategory, \
    SecuritySubCategory, Status


# Serializers define the API representation.
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductSecurityCapabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSecurityCapability
        fields = '__all__'


class SecurityCapabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityCapability
        fields = '__all__'


class SecurityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityCategory
        fields = '__all__'


class SecuritySubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SecuritySubCategory
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = '__all__'


# ViewSets define the view behavior.
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    filter_fields = ('id', 'name', 'published')
    search_fields = ('name', 'published')
    http_method_names = ['get', 'delete']


class ProductSecurityCapabilityViewSet(viewsets.ModelViewSet):
    queryset = ProductSecurityCapability.objects.all()
    serializer_class = ProductSecurityCapabilitySerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    search_fields = ('product__name', 'security_capability__name', 'security_capability__supporting_controls',
                     'status__name')
    filter_fields = ('product', 'details')


class SecurityCapabilityViewSet(viewsets.ModelViewSet):
    queryset = SecurityCapability.objects.all()
    serializer_class = SecurityCapabilitySerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    filter_fields = ('name', 'supporting_controls')
    search_fields = ('name', 'supporting_controls')


class SecurityCategoryViewSet(viewsets.ModelViewSet):
    queryset = SecurityCategory.objects.all()
    serializer_class = SecurityCategorySerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    filter_fields = ('name',)
    search_fields = ('name',)


class SecuritySubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SecuritySubCategory.objects.all()
    serializer_class = SecuritySubCategorySerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    filter_fields = ('name',)
    search_fields = ('name',)


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    filter_fields = ('name', 'value')
    search_fields = ('name',)


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'productsecuritycapabilities', ProductSecurityCapabilityViewSet)
router.register(r'securitycapabilities', SecurityCapabilityViewSet)
router.register(r'securitycategories', SecurityCategoryViewSet)
router.register(r'securitysubcategories', SecuritySubCategoryViewSet)
router.register(r'statuses', StatusViewSet)

urlpatterns = [
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'^businessunitsview', businessunitsview),
    url(r'^proddetailsview', proddetailsview),
    url(r'^health$', health),
    url(r'^productsview/', productsview),
    url(r'^submit', submit),

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
