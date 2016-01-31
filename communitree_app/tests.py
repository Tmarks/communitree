from django.test import TestCase
from .models import CropFeature, Pruning, Species, USDAZone
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
        self.assertEqual(cf.mpoly, mp)
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
        self.assertIsNotNone(pr)
        self.assertEqual(pr.crop_feature, cf)
        self.assertEqual(pr.completion_percentage, 0.1)


class SpeciesTests(TestCase):
    def test_create_Species(self):
        """Test the simplest creation of a Species.

        Needs a scientific name,
        common name,
        a USDA zone.
        """

        """
        estimated yield,
        recommended pruning windows yearly,
        harvest window
        are among other things it could have but doesn't require
        TODO: Add these anyway
        """

        sp = Species(scientific_name="Solanum lycopersicum",
                     common_name="Tomato",
                     usda_zone="4b")

        self.assertEqual(sp.scientific_name, "Solanum lycopersicum")
        self.assertEqual(sp.common_name, "Tomato")
        self.assertEqual(sp.usda_zone, "4b")

    """
    def test_invalid_choice_for_usda_zone(self):
        sp = Species(scientific_name="Solanum lycopersicum",
                     common_name="Tomato",
                     usda_zone="20")
                     """


class USDAZoneTests(TestCase):
    def test_create_USDAZone(self):
        """Test the simplest creation of a USDA Zone.

        It just needs the zone name.
        It's never going to be used by a user but it has to be done.
        """
        z = USDAZone(name="4a")
        self.assertEqual(z.name, "4a")



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
