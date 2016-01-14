from django.test import TestCase
from .models import CropFeature

# Create your tests here.

class CropFeatureTests(TestCase):
    def test_create_CropFeature(self):
        """Test the simplest creation of a CropFeature model.

        A crop feature at least needs a name and a MultiPolygon.
        At present we are going to allow a NULL Species. This test should be 
        updated if that changes.
        """

        cf = CropFeature.objects.create(name="Blueberry", mpoly="MULTIPOLYGON (((-71.239633 42.408400, -71.239621 42.408490, -71.239509 42.408486, -71.239509 42.408486, -71.239633 42.408400)))")
        cfq = CropFeature.objects.all()[0]
        self.assertIsNotNone(cfq)
        self.assertTrue(cfq.name == "Blueberry")
        
        #This, really is not very good. I know that.
        self.assertTrue(str(cfq.mpoly) == "MULTIPOLYGON (((-71.239633 42.408400, -71.239621 42.408490, -71.239509 42.408486, -71.239509 42.408486, -71.239633 42.408400)))")
        self.assertNone(cfq.species)


"""
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
"""
