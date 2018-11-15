from rest_framework import serializers
from scorecard import models


# Serializers define the API representation.
class BusinessUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BusinessUnit
        fields = '__all__'


class BusinessUnitGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BusinessUnitGroup
        fields = '__all__'


class BUScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BUScore
        fields = '__all__'


class BUGroupScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BUGroupScore
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Person
        fields = '__all__'


class ProductScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductScore
        fields = '__all__'


class ProductSecurityRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductSecurityRole
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'


class ProductSecurityCapabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductSecurityCapability
        fields = '__all__'


class SecurityCapabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SecurityCapability
        fields = '__all__'


class SecurityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SecurityCategory
        fields = '__all__'


class SecurityRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SecurityRole
        fields = '__all__'


class SecuritySubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SecuritySubCategory
        fields = '__all__'


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Status
        fields = '__all__'
