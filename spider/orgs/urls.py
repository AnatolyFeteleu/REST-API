"""spider URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from rest_framework import routers
from .views import (
    OrganizationView,
    OrganizationsListView,
    OrganizationDistrictView,
    DistrictEnterpriseView,
    DistrictEnterprisesView,
    #  ViewSets
    MerchandiseViewSet,

)


router = routers.SimpleRouter()
#  Cписок доступных товаров/услуг с возможностью поиска по доступным товарам/услугам и сортировка по цене
router.register(r'merchandises', MerchandiseViewSet)

urlpatterns = [
    #  Cписок всех организаций
    url(r'^organizations/$', OrganizationsListView.as_view(), name='organizations'),
    #  Информация об организациях и конкретной организации
    url(r'^organizations/organization_(?P<organization_id>.+)/$', OrganizationView.as_view(), name='organization_id'),
    #  Поиск организаций по району из общего списка районов через URL (organizations/district_<district_id>/...)
    url(r'^organizations/district_(?P<district_id>.+)/$', OrganizationDistrictView.as_view(),
        name='organization-district'),
    #  Cписок всех районов
    url(r'^districts/$', DistrictEnterprisesView.as_view()),
    #  Поиск организаций по району из общего списка районов через URL (districts/<district_id>/...)
    url(r'^districts/district_(?P<district_id>.+)/$', DistrictEnterpriseView.as_view()),

]

urlpatterns += router.urls
