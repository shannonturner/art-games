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

class LearnView(TemplateView):

    template_name = 'mash/learn.html'

    def get(self, request, **kwargs):

        " Displays all of the information returned by the API for each artwork. "

        art1 = request.GET.get('id1')
        art2 = request.GET.get('id2')

        try:
            art1 = int(art1)
        except:
            import random
            art1 = random.choice(Artwork.objects.all()).id

        try:
            art2 = int(art2)
        except:
            import random
            art2 = random.choice(Artwork.objects.all()).id

        artwork = []
        artwork.append(vars(Artwork.objects.get(id=art1)))
        artwork.append(vars(Artwork.objects.get(id=art2)))

        display_fields = ['title', 'artist', 'date', 'art_type', 'description', 'source', 'image_url', 'external_url', 'museum', 'from_api', 'dimensions', 'credit', 'accession', 'photo_credit']

        context = {
            'artwork': artwork,
            'display_fields': display_fields,
        }

        return render(request, self.template_name, context)
