from django.test import TestCase, Client
from django.urls import reverse
from .models import Car
from .forms import CarForm

class CarCrudTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.car = Car.objects.create(origin='USA', brand='Ferrari', model='F40', year='1992', color='Red', position=1)
        self.url_list = reverse('car_list')
        self.url_detail = reverse('car_detail', args=[self.car.pk])
        self.url_new = reverse('car_new')
        self.url_edit = reverse('car_edit', args=[self.car.pk])
        self.url_delete = reverse('car_delete', args=[self.car.pk])

    def test_car_detail_view(self):
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'car_detail.html')
        self.assertContains(response, self.car.model)

    def test_car_new_view(self):
        response = self.client.get(self.url_new)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'car_edit.html')

    def test_car_create(self):
        car_count_before = Car.objects.count()

        response = self.client.post(self.url_new, {
            'origin': 'Japan',
            'brand': 'Toyota',
            'model': 'Supra',
            'year': '2022',
            'color': 'Yellow'
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Car.objects.count(), car_count_before + 1)

    def test_car_edit_view(self):
        response = self.client.get(self.url_edit)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'car_edit.html')

    def test_car_update(self):
        car = Car.objects.create(origin='Japan', brand='Toyota', model='Supra', year='2022', color='Yellow', position=2)
        car_id = car.id

        response = self.client.post(reverse('car_edit', args=[car_id]), {
            'origin': 'Japan',
            'brand': 'Toyota',
            'model': 'Supra',
            'year': '2022',
            'color': 'Yellow',
            'position': 2
        })

        self.assertEqual(response.status_code, 302)
        updated_car = Car.objects.get(id=car_id)
        self.assertEqual(updated_car.origin, 'Japan')
        self.assertEqual(updated_car.brand, 'Toyota')
        self.assertEqual(updated_car.model, 'Supra')
        self.assertEqual(updated_car.year, '2022')
        self.assertEqual(updated_car.color, 'Yellow')
        self.assertEqual(updated_car.position, 2)

    def test_car_delete(self):
        car_count_before = Car.objects.count()

        response = self.client.post(self.url_delete)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Car.objects.count(), car_count_before - 1)
        
class UpdatePositionTestCase(TestCase):
    def setUp(self):
        self.car1 = Car.objects.create(origin='Japan', brand='Toyota', model='Camry', year='2022', color='Blue', position=1)
        self.car2 = Car.objects.create(origin='USA', brand='Ford', model='Mustang', year='2022', color='Red', position=2)

    def test_update_position(self):
        url = reverse('update_position')
        data = {
            'item_id': self.car1.id,
            'reference_item_id': self.car2.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

        # Verify that positions are swapped
        updated_car1 = Car.objects.get(id=self.car1.id)
        updated_car2 = Car.objects.get(id=self.car2.id)
        self.assertEqual(updated_car1.position, 2)
        self.assertEqual(updated_car2.position, 1)