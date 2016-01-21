from django.test import TestCase
from .models import CropFeature, Pruning
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon

# Create your tests here.

class CropFeatureTests(TestCase):
    def test_create_CropFeature(self):
        """Test the simplest creation of a CropFeature.

        A crop feature at least needs a name and a MultiPolygon.
        At present we are going to allow a NULL Species. This test should be 
        updated if that changes.
        """

        mp = GEOSGeometry("SRID=4326;MULTIPOLYGON (((-71.239633 42.408400, -71.239621 42.408490, -71.239509 42.408486, -71.239509 42.408486, -71.239633 42.408400)))")
        cf = CropFeature(name="Blueberry", mpoly=mp)
        self.assertIsNotNone(cf)
        self.assertTrue(cf.name == "Blueberry")
        self.assertEquals(cf.mpoly, mp)
        self.assertIsNone(cf.species)
    

class PruningTests(TestCase):
    def test_create_Pruning(self):
        """Test the simplest creation of a Pruning.

        Pruning needs a time and an approximate completion percentage.
        It maps to a CropFeature.
        Has a default DateTime of now().
        """

        mp = GEOSGeometry("SRID=4326;MULTIPOLYGON (((-71.239633 42.408400, -71.239621 42.408490, -71.239509 42.408486, -71.239509 42.408486, -71.239633 42.408400)))")
        cf = CropFeature(name="Blueberry", mpoly=mp)
        pr = Pruning(crop_feature=cf, completion_percentage=0.1)
        self.assertIsNotNone(prq)
        self.assertEquals(pr.crop_feature, cf)
        self.asssertEquals(pr.completion_percentage, 0.1)
      

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
