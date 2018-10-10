from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import OrderingFilter
from .models import Enterprise, Merchandise, District
from .serializers import (
    EnterpriseSerializer,
    MerchandiseSerializer,
    DistrictsSerializer,
    DistrictSerializer,
    EnterprisesSerializer,
)


# Class-based views
class OrganizationView(ListAPIView):
    serializer_class = EnterpriseSerializer

    def get_queryset(self):
        organization_id = self.kwargs['organization_id']
        enterprise = Enterprise.objects.filter(id=organization_id)
        return enterprise


class OrganizationDistrictView(ListAPIView):
    serializer_class = EnterpriseSerializer

    def get_queryset(self):
        district_id = self.kwargs['district_id']
        enterprise = Enterprise.objects.filter(district=district_id)
        return enterprise


class OrganizationsListView(ListAPIView):
    queryset = Enterprise.objects.all()
    serializer_class = EnterprisesSerializer


class DistrictEnterprisesView(ListAPIView):
    serializer_class = DistrictsSerializer
    queryset = District.objects.all()


class DistrictEnterpriseView(ListAPIView):
    serializer_class = DistrictSerializer

    def get_queryset(self):
        district = self.kwargs['district_id']
        query = Enterprise.objects.filter(district=district)
        return query


class MerchandiseViewSet(ReadOnlyModelViewSet):
    queryset = Merchandise.objects.all()
    serializer_class = MerchandiseSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('name', 'enterprise', 'price', 'category', 'sales_in')
    ordering_fields = ('price',)
