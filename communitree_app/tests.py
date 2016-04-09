from django.test import TestCase
from .models import CropFeature, Pruning, Species, USDAZone, PruningEvent
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon
from django.db import IntegrityError
from datetime import timedelta
from django.utils import timezone
import json

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
        At present we are going to allow a NULL Species.
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

    def test_set_active_PruningEvent(self):
        """Make sure we can set a PruningEvent as active on a cropfeature.

        This simply means setting active_pruningevent to a PruningEvent instance...
        """
        CropFeature.objects.create(name="Tasty Tomato nearby", mpoly=self.mp, species=self.sp)
        cfq = CropFeature.objects.all()[0]

        pe = PruningEvent.objects.create(cropfeature=cfq)

        cfq.active_pruningevent = pe
        cfq.save()

        cfq2 = CropFeature.objects.get()

        self.assertEqual(cfq2.active_pruningevent, pe)

    def test_turn_into_geojson(self):
        CropFeature.objects.create(name="Tasty Tomato nearby", mpoly=self.mp, species=self.sp)
        cfq = CropFeature.objects.all()[0]

        """
        Building expected output --
        Should be OK to use MultiPolygon.geojson because we're not really
        testing that. We're testing that other fields are added.
        We really don't want this to contain anything more than what's needed to
        display it on the map. Anything else, like the species info and the zone, should
        probably not be in "properties."
        The only extra thing we need is the CropFeature's primary key so the
        browser can get more information from the server when it's clicked.
        """
        expected = json.loads(self.mp.geojson)
        expected["properties"] = {}
        expected["properties"]["name"] = "Tasty Tomato nearby"
        expected["properties"]["pk"] = cfq.pk

        # CropFeature.geojson is a property -- we want to test that this returns the expected value.
        cropfeature_geojson = cfq.geojson

        self.assertEquals(cfq.geojson, expected)


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

    def tearDown(self):
        PruningEvent.objects.all().delete()


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

    def test_sum_completion_percentage_of_Prunings(self):
        PruningEvent.objects.create(cropfeature=self.cf)
        peq = PruningEvent.objects.all()[0]

        p = [Pruning.objects.create(pruningevent=peq, completion_percentage=x) for x in (0.1, 0.2, 0.3)]
        self.assertEqual(float(peq.get_completion_percentage()), 0.6)


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
