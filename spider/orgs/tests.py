from rest_framework.test import APIClient
from django.core.urlresolvers import reverse
from django.test import TestCase
from .models import Enterprise, District, EnterpriseNetwork, Merchandise, Category
import json


#  TestCase для проверки добавления данных в таблицу
class ModelTest(TestCase):
    def setUp(self):
        District.objects.create(name='District 1')
        self.district = District.objects.get(name='District 1').id

        EnterpriseNetwork.objects.create(name='Enterprise network 1')
        self.enterprise_network = EnterpriseNetwork.objects.get(name='Enterprise network 1').id

        self.enterprise = Enterprise(
            id=1,
            district=[self.enterprise_network],
            name='Enterprise 1',
            description='Description for Enterprise 1',
            affiliation=[self.enterprise_network],
        )

    def test_enterprise_model(self):
        old_count = Enterprise.objects.count()
        self.enterprise.save()
        new_count = Enterprise.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_merchandise_model(self):
        self.enterprise.save()

        Category.objects.create(name='Category 1')
        self.merchandise = Merchandise(
            id=1,
            name='Merchandise 1',
            category=Category.objects.get(name='Category 1'),
            price=250,
            enterprise=Enterprise.objects.get(name='Enterprise 1'),
            sales_in=[self.enterprise_network]
        )
        old_count_merch = Merchandise.objects.count()
        self.merchandise.save()
        new_count_merch = Merchandise.objects.count()
        self.assertNotEqual(old_count_merch, new_count_merch)


#  TestCase для проверки поиска организаций по району из общего списка районов
#  через URL (organizations/district_<district_id>/...)
class RestAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        District.objects.create(name='District 1')
        district = District.objects.get(name='District 1').id

        EnterpriseNetwork.objects.create(name='Enterprise network 1')
        enterprise_network = EnterpriseNetwork.objects.get(name='Enterprise network 1').id

        self.enterprise_name = 'Enterprise 1'
        enterprise_description = 'Description for Enterprise 1'

        Enterprise.objects.create(
            id=1,
            district=[district],
            name=self.enterprise_name,
            description=enterprise_description,
            affiliation=[enterprise_network],
        )

    def test_returning_data(self):
        enterprise = Enterprise.objects.get(name=self.enterprise_name)
        response = self.client.get(
            reverse('organization-district', args=[enterprise.id])
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            enterprise
        )


#  TestCase для проверки информации о товаре или услуги
class MerchDetailsTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        District.objects.create(name='District 1')
        self.district = District.objects.get(name='District 1')

        enterprise_name = 'Enterprise 1'
        enterprise_description = 'Description for Enterprise 1'

        EnterpriseNetwork.objects.create(name='Enterprise network 1')
        self.enterprise_network = EnterpriseNetwork.objects.get(name='Enterprise network 1').id

        Category.objects.create(name='Category 1')

        Enterprise.objects.create(
            id=1,
            district=[self.enterprise_network],
            name=enterprise_name,
            description=enterprise_description,
            affiliation=[self.enterprise_network],
        )
        self.enterprise_obj = Enterprise.objects.get(name=enterprise_name)

        self.merch_name = 'Merchandise 1'
        self.merch_category = Category.objects.get(name='Category 1')
        self.merch_price = 250
        self.merch_id = 1

        Merchandise.objects.create(
            id=self.merch_id,
            name=self.merch_name,
            category=self.merch_category,
            price=self.merch_price,
            enterprise=self.enterprise_obj,
            sales_in=[self.enterprise_network]
        )

    def test_merch_details(self):
        merchandise = Merchandise.objects.get(name=self.merch_name)
        response = self.client.get(
            reverse('merchandise-detail', args=[merchandise.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, {
            'id': self.merch_id,
            'name': self.merch_name,
            'category': self.merch_category.name,
            'price': self.merch_price,
            'enterprise_id': self.enterprise_obj.id,
            'enterprise_name': self.enterprise_obj.name
        })


#  TestCase для проверки информации об организации
class EnterpriseDetailsTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        EnterpriseNetwork.objects.create(name='Enterprise network 1')
        self.enterprise_network = EnterpriseNetwork.objects.get(name='Enterprise network 1').id
        self.enterprise_name = 'Enterprise 1'
        Enterprise.objects.create(
            id=1,
            district=[self.enterprise_network],
            name='Enterprise 1',
            description='Description for Enterprise 1',
            affiliation=[self.enterprise_network],
        )

    def test_enterprise_details(self):
        enterprise = Enterprise.objects.get(name=self.enterprise_name)
        response = self.client.get(
            reverse('organization_id', args=[enterprise.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, enterprise)


#  TestCase для проверки списка доступных организаций
class EnterpriseListTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        #  Создание обьектов для модели "Районы"
        District.objects.create(name='District 1')
        self.district_1 = District.objects.get(name='District 1').id

        District.objects.create(name='District 2')
        self.district_2 = District.objects.get(name='District 2').id

        #  Создание обьектов для модели "Сеть предприятий"
        EnterpriseNetwork.objects.create(name='Enterprise network 1')
        self.enterprise_network_1 = EnterpriseNetwork.objects.get(name='Enterprise network 1').id

        EnterpriseNetwork.objects.create(name='Enterprise network 2')
        self.enterprise_network_2 = EnterpriseNetwork.objects.get(name='Enterprise network 2').id

        #  Предприятия 1
        self.enterprise_name_1 = 'Enterprise 1'
        Enterprise.objects.create(
            id=1,
            district=[self.district_1],
            name=self.enterprise_name_1,
            description='Description for Enterprise 1',
            affiliation=[self.enterprise_network_1],
        )

        #  Предприятие 2
        self.enterprise_name_2 = 'Enterprise 2'
        Enterprise.objects.create(
            id=2,
            district=[self.district_1],
            name=self.enterprise_name_2,
            description='Description for Enterprise 2',
            affiliation=[self.enterprise_network_2],
        )

        #  Предприятие 3
        self.enterprise_name_3 = 'Enterprise 3'
        Enterprise.objects.create(
            id=3,
            district=[self.district_2],
            name=self.enterprise_name_3,
            description='Description for Enterprise 3',
            affiliation=[self.enterprise_network_1],
        )

        #  Предприятие 4
        self.enterprise_name_4 = 'Enterprise 4'
        Enterprise.objects.create(
            id=4,
            district=[self.district_2],
            name=self.enterprise_name_4,
            description='Description for Enterprise 4',
            affiliation=[self.enterprise_network_2],
        )

    def test_get_companies_list(self):
        enterprises = Enterprise.objects.all().values('name')
        response = self.client.get(
            reverse('organizations'),
        )
        response_list = list()
        for i in json.loads(response.content):
            response_list.append({'name': i['name']})

        self.assertEqual(response.status_code, 200)
        self.assertListEqual(
            response_list,
            list(enterprises)
        )
