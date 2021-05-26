from django.test import TestCase
from .models import *

class InventarTestCase(TestCase):
    def setUp(self):
        t1 = HardwareClass.objects.create(name="Keyboards")
        t2 = HardwareClass.objects.create(name="Display")
        o1 = Article.objects.create(name="Keyboard", ean=12345678, hardwareClass=t1)
        o2 = Article.objects.create(name="Monitor", ean=64729352, hardwareClass=HardwareClass.objects.get(name="Display"))

        Equipment.objects.create(base=o1, sn="245ABT789", inventarNr=123)


        u1 = Customer.objects.create(name="Klaus")
        u2 = Customer.objects.create(name="Peter")

        w1 = Workplace.objects.create(place="AP1", room="01.34")

        h1 = Handover.objects.create(user_content_type = ContentType.objects.get_for_model(u1), user_object_id = u1.pk)

    def test_inventar(self):
        o1 = Article.objects.get(name="Keyboard")
        o2 = Article.objects.get(ean=64729352)

        self.assertEqual(o1.ean, 12345678)
        self.assertEqual(o2.name, "Monitor")
        self.assertEqual(o1.status, Article.ArticleStatusType.NEW)
        self.assertNotEqual(o2.status, Article.ArticleStatusType.ACTIVE)

        e1 = Equipment.objects.get(inventarNr=123)
        self.assertEqual(e1.base.name, "Keyboard")

        self.assertEqual(o1.__str__(), "Keyboards : Keyboard")
        self.assertEqual(e1.__str__(), "Keyboards : Keyboard (245ABT789)")

        self.assertEqual(Article.objects.count(), 2)


        w1 = Workplace.objects.get(room="01.34")
        self.assertEqual(w1.__str__(), "01.34 - AP1")

        h1 = Handover.objects.first()
        self.assertEqual(h1.user.__str__(), "Klaus")

