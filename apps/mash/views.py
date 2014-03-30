from django.shortcuts import render
from django.views.generic.base import TemplateView

from apps.mash.models import Vote

class MashView(TemplateView):

    template_name = 'mash/mash.html'

    def get(self, request, **kwargs):

        " Display two artworks side by side. "

        context = self.get_context_data(**kwargs)
        return render(request, template_name, context)

    def post(self, request, **kwargs):

        " Handle voting and display two artworks side by side. "
        
        won = kwargs.get('won')
        lost = kwargs.get('lost')

        try:
            won = int(won)
            lost = int(lost)
        except:
            won, lost = False, False

        if won and lost:
            vote = Vote(**{'won': won, 'lost': lost})
            vote.save()

        context = self.get_context_data(**kwargs)
        return render(request, template_name, context)

    def get_context_data(**kwargs):

        " Determine which two artworks should be displayed side by side and return them as context. "

        from get_artworks import get_artworks

        specific_apis = kwargs.get('specific_apis') # For when user has limited the APIs to source artworks from

        if specific_apis:
            raise NotImplementedError # Not yet, that is.  TODO

        return get_artworks(**{'specific_apis': specific_apis})