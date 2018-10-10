from rest_framework import serializers
from .models import Enterprise, Merchandise, District


class EnterpriseSerializer(serializers.ModelSerializer):
    district_name = serializers.StringRelatedField(source='district', many=True)
    enterprise_id = serializers.IntegerField(source='id')

    class Meta:
        model = Enterprise
        fields = ('enterprise_id', 'name', 'description', 'district', 'district_name')


class EnterprisesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = ('id', 'name', 'district')


class MerchandiseSerializer(serializers.ModelSerializer):
    enterprise_name = serializers.CharField(source='enterprise')
    enterprise_id = serializers.IntegerField(source='enterprise.id')
    category = serializers.StringRelatedField()

    class Meta:
        model = Merchandise
        fields = ('id', 'name', 'category', 'price', 'enterprise_id', 'enterprise_name')


class DistrictsSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    enterprise_id = serializers.CharField(source='id')
    enterprise_name = serializers.CharField(source='name')

    class Meta:
        model = District
        fields = ('enterprise_id', 'enterprise_name')

