from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import View
from django.core import serializers
from django.core.urlresolvers import reverse
from .models import CropFeature

from .forms import FaceForm


class Index(View):
    def get(self, request):
        return render(request, "communitree_app/index.html")


class Viewy(View):
    def get(self, request):
        form = FaceForm()
        return render(request, "communitree_app/face.html", {'form': form})

    def post(self, request):
        form = FaceForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(reverse("communitree_app:facemake"))


class Facemake(View):
    def get(self, request):
        form = FaceForm(request.POST)
        # already validated in Viewy.post()?
        # uh
        return JsonResponse({'foo':'bar'})


class QueryDB(View):
    def get(self, request):
        return JsonResponse({"cropfeature" : CropFeature.objects.last().mpoly.geojson})

