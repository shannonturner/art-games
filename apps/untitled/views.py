from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.template import RequestContext
from django.db.models import Q
from django.http import HttpResponseRedirect

from apps.mash.models import Artwork, Vote
from apps.untitled.models import NewTitle

# Create your views here.

class UntitledView(TemplateView):

    " View for the 'Untitled' Game "

    template_name = 'untitled/untitled.html'

    def get(self, request, **kwargs):

        " Display one artwork whose official title contains 'Untitled' "

        context = self.get_context_data(**{'uid': request.GET.get('uid'), 'id': request.GET.get('id')})
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):

        " Submit a new title for an artwork whose official title contains 'Untitled' "

        import string
        
        artwork_id = request.POST.get('id')
        title = request.POST.get('title')
        
        try:
            artwork_id = int(artwork_id)
            title = str(title)
        except:
            artwork_id, title = False, False

        if len(title) > 60:
            title = title[:57] + '...'

        allowed_chars = string.ascii_letters + string.digits + ' -~!@#$%^&()-+?,.'
        title = ''.join([char for char in title if char in allowed_chars])

        if artwork_id and title:
            newtitle = NewTitle(**{'title': title, 'art': Artwork.objects.get(id=artwork_id)})
            newtitle.save()

        return HttpResponseRedirect('/art/untitled?uid={0}'.format(newtitle.id))

    def get_context_data(self, **kwargs):

        """ If uid is passed, display that NewTitle along with the artwork. 
            Or if id is passed, display a specific artwork.
            Otherwise, get a random artwork that's untitled.
        """

        import urllib

        artwork = False
        title = ''
        has_actual_title = False
        newtitle_id = False

        if kwargs.get('uid'):
            try:
                newtitle_id = int(kwargs.get('uid'))
                newtitle = NewTitle.objects.get(id=newtitle_id)
                title = newtitle.title
                artwork = Artwork.objects.get(id=newtitle.art_id)
            except:
                pass # artwork is still False
        elif kwargs.get('id'): # elif because sharing an existing title takes priority
            try:
                art_id = int(kwargs.get('id'))
                artwork = Artwork.objects.get(id=art_id)
                # In cases where an artwork with a title is specified, use the actual title
                if 'ntitled' in artwork.title or not artwork.title:
                    title = ''
                else:
                    has_actual_title = True
                    title = artwork.title 
            except:
                pass # artwork is still false

        if not artwork: # no uid/id passed or it was invalid
            import random
            available_artworks = Artwork.objects.filter(
                Q(title='') | Q(title__icontains='Untitled') | Q(title__isnull=True)
                )
            artwork = random.choice(available_artworks)

        try:
            urlsafe_title = urllib.quote(title)
        except:
            urlsafe_title = urllib.quote(title.encode('utf-8'))

        context = {
            'artwork': artwork,
            'title': title,
            'urlsafe_title': urlsafe_title,
            'actual': has_actual_title,
            'newtitle_id': newtitle_id,
        }

        return context