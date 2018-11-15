from django_filters import rest_framework
from rest_framework import filters, viewsets
from scorecard import api_serializers
from scorecard import models


# ViewSets define the view behavior.
class BusinessUnitViewSet(viewsets.ModelViewSet):
    queryset = models.BusinessUnit.objects.all()
    serializer_class = api_serializers.BusinessUnitSerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    filter_fields = ('id', 'name', 'bu_group', 'pp_id')
    search_fields = ('name',)
    http_method_names = ['get', 'delete']


class BusinessUnitGroupViewSet(viewsets.ModelViewSet):
    queryset = models.BusinessUnitGroup.objects.all()
    serializer_class = api_serializers.BusinessUnitGroupSerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    filter_fields = ('id', 'name', 'pp_id')
    search_fields = ('name',)
    http_method_names = ['get', 'delete']


class BUScoreViewSet(viewsets.ModelViewSet):
    queryset = models.BUScore.objects.all()
    serializer_class = api_serializers.BUScoreSerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    filter_fields = ('id', 'score', 'max_score', 'bu')
    http_method_names = ['get', 'delete']


class BUGroupScoreViewSet(viewsets.ModelViewSet):
    queryset = models.BUGroupScore.objects.all()
    serializer_class = api_serializers.BUGroupScoreSerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    filter_fields = ('id', 'score', 'max_score', 'bu_group')
    http_method_names = ['get', 'delete']


class PersonViewSet(viewsets.ModelViewSet):
    queryset = models.Person.objects.all()
    serializer_class = api_serializers.PersonSerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    filter_fields = ('id', 'full_name', 'email', 'username', 'pp_id')
    search_fields = ('full_name', 'email', 'username')
    http_method_names = ['get', 'delete']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = api_serializers.ProductSerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    filter_fields = ('id', 'name', 'published', 'pp_id')
    search_fields = ('name', 'published')
    http_method_names = ['get', 'delete']


class ProductScoreViewSet(viewsets.ModelViewSet):
    queryset = models.ProductScore.objects.all()
    serializer_class = api_serializers.ProductScoreSerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    filter_fields = ('id', 'category', 'score', 'max_score', 'product')
    search_fields = ('category',)
    http_method_names = ['get', 'delete']


class ProductSecurityCapabilityViewSet(viewsets.ModelViewSet):
    queryset = models.ProductSecurityCapability.objects.all()
    serializer_class = api_serializers.ProductSecurityCapabilitySerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    search_fields = ('product__name', 'security_capability__name', 'security_capability__supporting_controls',
                     'status__name')
    filter_fields = ('product', 'details')


class ProductSecurityRoleViewSet(viewsets.ModelViewSet):
    queryset = models.ProductSecurityRole.objects.all()
    serializer_class = api_serializers.ProductSecurityRoleSerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    filter_fields = ('role', 'product', 'person')


class SecurityCapabilityViewSet(viewsets.ModelViewSet):
    queryset = models.SecurityCapability.objects.all()
    serializer_class = api_serializers.SecurityCapabilitySerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    filter_fields = ('name', 'supporting_controls')
    search_fields = ('name', 'supporting_controls')


class SecurityCategoryViewSet(viewsets.ModelViewSet):
    queryset = models.SecurityCategory.objects.all()
    serializer_class = api_serializers.SecurityCategorySerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    filter_fields = ('name',)
    search_fields = ('name',)


class SecurityRoleViewSet(viewsets.ModelViewSet):
    queryset = models.SecurityRole.objects.all()
    serializer_class = api_serializers.SecurityRoleSerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    filter_fields = ('description', 'function')
    search_fields = ('description', 'function')


class SecuritySubCategoryViewSet(viewsets.ModelViewSet):
    queryset = models.SecuritySubCategory.objects.all()
    serializer_class = api_serializers.SecuritySubCategorySerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    filter_fields = ('name',)
    search_fields = ('name',)


class StatusViewSet(viewsets.ModelViewSet):
    queryset = models.Status.objects.all()
    serializer_class = api_serializers.StatusSerializer
    filter_backends = (filters.SearchFilter, rest_framework.DjangoFilterBackend)
    filter_fields = ('name', 'value')
    search_fields = ('name',)
