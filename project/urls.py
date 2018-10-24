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
from scorecard.models import BusinessUnit, BusinessUnitGroup, BUScore, Product, ProductSecurityCapability, Person, \
    ProductScore, ProductSecurityRole, SecurityCapability, SecurityCategory, SecurityRole, SecuritySubCategory, Status


# Serializers define the API representation.
class BusinessUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessUnit
        fields = '__all__'


class BusinessUnitGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessUnitGroup
        fields = '__all__'


class BUScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = BUScore
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class ProductScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductScore
        fields = '__all__'


class ProductSecurityRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSecurityRole
        fields = '__all__'


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


class SecurityRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityRole
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
class BusinessUnitViewSet(viewsets.ModelViewSet):
    queryset = BusinessUnit.objects.all()
    serializer_class = BusinessUnitSerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    filter_fields = ('id', 'name', 'bu_group', 'pp_id')
    search_fields = ('name',)
    http_method_names = ['get', 'delete']


class BusinessUnitGroupViewSet(viewsets.ModelViewSet):
    queryset = BusinessUnitGroup.objects.all()
    serializer_class = BusinessUnitGroupSerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    filter_fields = ('id', 'name', 'pp_id')
    search_fields = ('name',)
    http_method_names = ['get', 'delete']


class BUScoreViewSet(viewsets.ModelViewSet):
    queryset = BUScore.objects.all()
    serializer_class = BUScoreSerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    filter_fields = ('id', 'score', 'max_score', 'bu')
    http_method_names = ['get', 'delete']


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    filter_fields = ('id', 'full_name', 'email', 'username', 'pp_id')
    search_fields = ('full_name', 'email', 'username')
    http_method_names = ['get', 'delete']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    filter_fields = ('id', 'name', 'published', 'pp_id')
    search_fields = ('name', 'published')
    http_method_names = ['get', 'delete']


class ProductScoreViewSet(viewsets.ModelViewSet):
    queryset = ProductScore.objects.all()
    serializer_class = ProductScoreSerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    filter_fields = ('id', 'category', 'score', 'max_score', 'product')
    search_fields = ('category',)
    http_method_names = ['get', 'delete']


class ProductSecurityCapabilityViewSet(viewsets.ModelViewSet):
    queryset = ProductSecurityCapability.objects.all()
    serializer_class = ProductSecurityCapabilitySerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    search_fields = ('product__name', 'security_capability__name', 'security_capability__supporting_controls',
                     'status__name')
    filter_fields = ('product', 'details')


class ProductSecurityRoleViewSet(viewsets.ModelViewSet):
    queryset = ProductSecurityRole.objects.all()
    serializer_class = ProductSecurityRoleSerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    filter_fields = ('role', 'product', 'person')


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


class SecurityRoleViewSet(viewsets.ModelViewSet):
    queryset = SecurityRole.objects.all()
    serializer_class = SecurityRoleSerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    filter_fields = ('description', 'function')
    search_fields = ('description', 'function')


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
router.register(r'businessunits', BusinessUnitViewSet)
router.register(r'businessunitgroups', BusinessUnitGroupViewSet)
router.register(r'buscores', BUScoreViewSet)
router.register(r'persons', PersonViewSet)
router.register(r'products', ProductViewSet)
router.register(r'productscores', ProductScoreViewSet)
router.register(r'productsecuritycapabilities', ProductSecurityCapabilityViewSet)
router.register(r'productsecurityroles', ProductSecurityRoleViewSet)
router.register(r'securitycapabilities', SecurityCapabilityViewSet)
router.register(r'securitycategories', SecurityCategoryViewSet)
router.register(r'securityroles', SecurityRoleViewSet)
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
