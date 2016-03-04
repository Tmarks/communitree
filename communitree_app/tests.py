from django.test import TestCase
from .models import CropFeature, Pruning, Species, USDAZone, PruningEvent
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
from django.db import IntegrityError
from datetime import timedelta
from django.utils import timezone

# Create your tests here.


class CropFeatureTests(TestCase):
    def setUp(self):
        self.mp = GEOSGeometry("SRID=4326;MULTIPOLYGON (((-71.239633 42.408400, "
                          "-71.239621 42.408490, "
                          "-71.239509 42.408486, "
                          "-71.239509 42.408486, "
                          "-71.239633 42.408400)))")

        self.sp = Species.objects.create(scientific_name="Solanum lycopersicum",
                                    common_name="Tomato")

    def tearDown(self):
        Species.objects.all().delete()

    def test_create_CropFeature(self):
        """Test the simplest creation of a CropFeature.

        A crop feature at least needs a name and a MultiPolygon.
        At present we are going to allow a NULL Species. This test should be 
        updated if that changes.
        """

        cf = CropFeature.objects.create(name="Blueberry", mpoly=self.mp)
        self.assertIsNotNone(cf)
        self.assertEqual(cf.name, "Blueberry")
        self.assertEqual(cf.mpoly, self.mp)
        self.assertIsNone(cf.species)

    def test_get_Species_from_CropFeature(self):
        """Test getting the Species reference from a CropFeature."""
        # Current minimum requirements for CropFeature are geometry and name
        # so we must include these.
        CropFeature.objects.create(name="Tasty Tomato nearby", mpoly=self.mp, species=self.sp)
        cfq = CropFeature.objects.all()[0]

        # but we only need test the species
        self.assertEqual(cfq.species, self.sp)


class PruningTests(TestCase):
    """Tests of classes/functions that are meant to implement the pruning tracking functionality"""

    def setUp(self):
        # A Pruning must be associated with a PruningEvent. That is the foreign key.
        # So make one here.
        mp = GEOSGeometry("SRID=4326;MULTIPOLYGON (((-71.239633 42.408400, -71.239621 42.408490, -71.239509 42.408486, -71.239509 42.408486, -71.239633 42.408400)))")
        cf = CropFeature.objects.create(name="Blueberry", mpoly=mp)
        self.pe = PruningEvent.objects.create(cropfeature=cf)

    def test_create_Pruning(self):
        """Test the simplest creation of a Pruning.

        Pruning needs a time and an approximate completion percentage.
        It maps to a PruningEvent.
        Has a default DateTime of now().
        """

        pr = Pruning.objects.create(pruningevent=self.pe, completion_percentage=0.1)
        self.assertIsNotNone(pr)
        self.assertEqual(pr.pruningevent, self.pe)
        self.assertEqual(pr.completion_percentage, 0.1)


class PruningEventTests(TestCase):
    def setUp(self):

        # it needs a CropFeature, which needs a multipolygon...
        mp = GEOSGeometry("SRID=4326;MULTIPOLYGON (((-71.239633 42.408400, "
                          "-71.239621 42.408490, "
                          "-71.239509 42.408486, "
                          "-71.239509 42.408486, "
                          "-71.239633 42.408400)))")
        self.cf = CropFeature.objects.create(name="Blueberry", mpoly=mp)


    def test_create_PruningEvent(self):
        """PruningEvent creation, simplest case
        Has a start_time (by default, time of event creation),
        and a CropFeature it's associated with.
        """

        PruningEvent.objects.create(cropfeature=self.cf)
        peq = PruningEvent.objects.all()[0]

        self.assertIsNotNone(peq.start_time)
        self.assertEqual(peq.cropfeature, self.cf)

    def test_start_time_on_new_PruningEvent(self):
        # It shouldn't take even five seconds to make this object so we test
        # that it's within five seconds. It's sufficient.
        fiveseconds = timedelta(seconds=5)

        # A PruningEvent's default start time is "now"
        PruningEvent.objects.create(cropfeature=self.cf)
        peq = PruningEvent.objects.all()[0]
        self.assertTrue(timezone.now() - peq.start_time < fiveseconds)


class SpeciesTests(TestCase):
    """ """
    @classmethod
    def setUpClass(cls):
        """Set up for testing the Species relation (and related tables).

        These tests require that there exist entries in the USDAZone table.
        So we must make some here.
        """
        for s in [str(x)+y for x in range(1, 14) for y in 'ab']:
            USDAZone.objects.create(name=s)

    @classmethod
    def tearDownClass(cls):
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
