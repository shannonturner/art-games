from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.template import RequestContext

from apps.mash.models import Artwork, Vote

class MashView(TemplateView):

    template_name = 'mash/mash.html'

    def get(self, request, **kwargs):

        " Display two artworks side by side. "

        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):

        " Handle voting and display two artworks side by side. "
        
        won = request.POST.get('won')
        lost = request.POST.get('lost')

        try:
            won = int(won)
            lost = int(lost)
        except:
            won, lost = False, False

        if won and lost:
            vote = Vote(**{'won': Artwork.objects.get(id=won), 'lost': Artwork.objects.get(id=lost)})
            vote.save()

        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):

        " Determine which two artworks should be displayed side by side and return them as context. "

        from get_artworks import get_artworks

        specific_apis = request.POST.get('specific_apis') # For when user has limited the APIs to source artworks from

        if specific_apis:
            raise NotImplementedError # Not yet, that is.  TODO

        artworks = {}

        for index, artwork in enumerate(get_artworks(**{'specific_apis': specific_apis})):
            artworks['art{0}'.format(index)] = artwork

        return artworks