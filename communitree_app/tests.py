from django.test import TestCase
from .models import CropFeature, Pruning, Species, USDAZone
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
from django.db import IntegrityError

# Create your tests here.


class CropFeatureTests(TestCase):
    def test_create_CropFeature(self):
        """Test the simplest creation of a CropFeature.

        A crop feature at least needs a name and a MultiPolygon.
        At present we are going to allow a NULL Species. This test should be 
        updated if that changes.
        """

        mp = GEOSGeometry("SRID=4326;MULTIPOLYGON (((-71.239633 42.408400, -71.239621 42.408490, -71.239509 42.408486, -71.239509 42.408486, -71.239633 42.408400)))")
        cf = CropFeature.objects.create(name="Blueberry", mpoly=mp)
        self.assertIsNotNone(cf)
        self.assertTrue(cf.name == "Blueberry")
        self.assertEqual(cf.mpoly, mp)
        self.assertIsNone(cf.species)

    def test_get_Species_from_CropFeature(self):
        """Test getting the Species reference from a CropFeature."""
        mp = GEOSGeometry("SRID=4326;MULTIPOLYGON (((-71.239633 42.408400, "
                          "-71.239621 42.408490, "
                          "-71.239509 42.408486, "
                          "-71.239509 42.408486, "
                          "-71.239633 42.408400)))")

        sp = Species.objects.create(scientific_name="Solanum lycopersicum",
                                    common_name="Tomato")

        # Current minimum requirements for CropFeature are geometry and name
        # so we must include these.
        cf = CropFeature.objects.create(name="Tasty Tomato nearby", mpoly=mp, species=sp)
        cfq = CropFeature.objects.all()[0]

        # but we only need test the species
        self.assertEqual(cfq.species, sp)


class PruningTests(TestCase):
    def test_create_Pruning(self):
        """Test the simplest creation of a Pruning.

        Pruning needs a time and an approximate completion percentage.
        It maps to a CropFeature.
        Has a default DateTime of now().
        """

        mp = GEOSGeometry("SRID=4326;MULTIPOLYGON (((-71.239633 42.408400, -71.239621 42.408490, -71.239509 42.408486, -71.239509 42.408486, -71.239633 42.408400)))")
        cf = CropFeature.objects.create(name="Blueberry", mpoly=mp)
        pr = Pruning.objects.create(crop_feature=cf, completion_percentage=0.1)
        self.assertIsNotNone(pr)
        self.assertEqual(pr.crop_feature, cf)
        self.assertEqual(pr.completion_percentage, 0.1)


class SpeciesTests(TestCase):
    """ """
    def setUp(self):
        """Set up for testing the Species relation (and related tables).

        These tests require that there exist entries in the USDAZone table.
        So we must make some here.
        """
        USDAZone.objects.create(name="1a")
        USDAZone.objects.create(name="1b")
        USDAZone.objects.create(name="2a")
        USDAZone.objects.create(name="2b")
        USDAZone.objects.create(name="3a")
        USDAZone.objects.create(name="3b")
        USDAZone.objects.create(name="4a")
        USDAZone.objects.create(name="4b")
        USDAZone.objects.create(name="5a")
        USDAZone.objects.create(name="5b")
        USDAZone.objects.create(name="6a")
        USDAZone.objects.create(name="6b")
        USDAZone.objects.create(name="7a")
        USDAZone.objects.create(name="7b")
        USDAZone.objects.create(name="8a")
        USDAZone.objects.create(name="8b")
        USDAZone.objects.create(name="9a")
        USDAZone.objects.create(name="9b")
        USDAZone.objects.create(name="10a")
        USDAZone.objects.create(name="10b")
        USDAZone.objects.create(name="11a")
        USDAZone.objects.create(name="11b")
        USDAZone.objects.create(name="12a")
        USDAZone.objects.create(name="12b")
        USDAZone.objects.create(name="13a")
        USDAZone.objects.create(name="13b")

    def tearDown(self):
        USDAZone.objects.all().delete()

    def test_create_Species(self):
        """Test the simplest creation of a Species.

        Needs a scientific name,
        common name,
        a reference to a USDAZone.
        """

        """
        estimated yield,
        recommended pruning windows yearly,
        harvest window
        are among other things it could have but doesn't require
        TODO: Add these anyway
        """

        sp = Species.objects.create(scientific_name="Solanum lycopersicum",
                                    common_name="Tomato")

        sp.usda_zones.add(USDAZone.objects.get(name="4a"))

        self.assertEqual(sp.scientific_name, "Solanum lycopersicum")
        self.assertEqual(sp.common_name, "Tomato")

        z4a = USDAZone.objects.get(name="4a")
        self.assertTrue(z4a in sp.usda_zones.all())

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
        This way, there is room for it to grow. We could possibly add data to a Zone. Like, perhaps which states
        fall into it.
        Or maybe even make geometry for it. Oh wait. That actually sounds important now that I say it.
        """
        z = USDAZone.objects.create(name="4a")
        self.assertEqual(z.name, "4a")

    def test_USDAZone_name_is_unique(self):
        """This test probably isn't really good or necessary but I needed to write it before making this change."""
        USDAZone.objects.create(name="4a")
        self.assertRaises(IntegrityError, USDAZone.objects.create, name="4a")






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
