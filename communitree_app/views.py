from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import View
from django.core.urlresolvers import reverse

from .forms import FaceForm


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
