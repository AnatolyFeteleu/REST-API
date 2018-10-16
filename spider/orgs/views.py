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
        organization_id = self.kwargs.get('organization_id')
        enterprise = Enterprise.objects.all().filter(id=organization_id)
        return enterprise


class MerchandiseListView(ListAPIView):
    queryset = Merchandise.objects.select_related('category').select_related('merch').all()
    serializer_class = MerchandiseSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filter_fields = ('merch__name', 'enterprise', 'price', 'category')
    ordering_fields = ('price',)


class MerchandiseView(ListAPIView):
    queryset = Merchandise.objects.select_related('category').all()

    def get_queryset(self):
        merch_id = self.kwargs.get('merch_id')
        merchandise = Merchandise.objects.filter(id=merch_id)
        return merchandise


class OrganizationDistrictView(ListAPIView):
    serializer_class = EnterpriseSerializer

    def get_queryset(self):
        district_id = self.kwargs.get('district_id')
        enterprise = Enterprise.objects.prefetch_related('district').filter(district=district_id)
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
        district = self.kwargs.get('district_id')
        query = Enterprise.objects.filter(district=district)
        return query
