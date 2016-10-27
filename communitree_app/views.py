from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.core import serializers
from .models import CropFeature
import json
from django.contrib.gis.geos import Polygon

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from .forms import FaceForm


class Index(View):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        return render(request, "communitree_app/index.html")


class Crops(View):
    def get(self, request, **kwargs):
        if 'id' in kwargs and kwargs['id'] != '':
            try:
                crop = CropFeature.objects.get(id=kwargs['id'])
                crop_json = crop.geojson

                #This is easier to handle on the client side. We need strings
                #to display, so why not just send empty strings from here if
                #that's what needs to happen?
                species = {
                    "scientific_name": "",
                    "common_name": ""
                }
                if crop.species is not None:
                    if crop.species.scientific_name is not None:
                        species["scientific_name"] = crop.species.scientific_name
                    if crop.species.common_name is not None:
                        species["common_name"] = crop.species.common_name
                crop_json["properties"]["species"] = species;

                if crop.active_pruningevent is not None:
                    pruning_event = {"start_time": crop.active_pruningevent.start_time}
                    recent_prunings = [dict(log_time=p.log_time, completion_percentage=p.completion_percentage) for p in crop.active_pruningevent.pruning_set.order_by('-log_time')]
                else:
                    pruning_event = None
                    recent_prunings = []

                crop_json["properties"]["pruning_event"] = pruning_event
                crop_json["properties"]["recent_prunings"] = recent_prunings

                return JsonResponse(crop_json)

            except CropFeature.DoesNotExist:
                raise Http404("The requested crop does not exist.")
        else:
            #TODO: I'm not sure what to do about this. For now, I'm just going to give it SOMEthing to do.
            #As of the moment though, I don't have a use case for getting CropFeatures in some order they happen to
            #come in when retrieved from the database.
            return JsonResponse([cf.geojson for cf in CropFeature.objects.all()[:100]], safe=False)


class CropsByBounds(View):
    def get(self, request):
        if 'bounds' in request.GET:
            # request.GET['bounds'] is the return value from LeafletJS's
            # Map.getBounds().toBBoxString().
            # That's 'southwest_lng,southwest_lat,northeast_lng,northeast_lat'
            # So this fits what Polygon.from_bbox expects.
            # ... except I think if the box crosses the International Date Line, or
            # if it would contain a pole.
            # TODO: Might be worth figuring this out some day, though no one's
            # gonna find any blueberries in the middle of the pacific or at the
            # South Pole.
            bounds = [float(x) for x in request.GET['bounds'].split(',')]

            bounds_polygon = Polygon.from_bbox(bounds)
            cropfeatures_in_view = [cf.geojson for cf in CropFeature.objects.filter(mpoly__intersects=bounds_polygon)]
            return JsonResponse(cropfeatures_in_view, safe=False)
        else:
            #TODO: Figure out the proper way to handle this.
            raise Exception("'bounds' not found in the HTTP GET parameters.")


