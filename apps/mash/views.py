from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.template import RequestContext

from apps.mash.models import Artwork, Vote

class HomeView(TemplateView):

    template_name = 'home.html'

    def get(self, request, **kwargs):

        context = {}

        return render(request, self.template_name, context)

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

        # specific_apis = request.POST.get('specific_apis') # For when user has limited the APIs to source artworks from
        specific_apis = None

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

class MashFavoritesView(TemplateView):

    template_name = 'mash/favorites.html'

    def get(self, request, **kwargs):

        " Displays the top 10 favorites in the system. "

        from django.db.models import Count

        display_fields = ['title', 'artist', 'date', 'art_type', 'description', 'source', 'image_url', 'external_url', 'museum', 'from_api', 'dimensions', 'credit', 'accession', 'photo_credit']

        records_by_id = Artwork.objects.values('id').annotate(Count('won__id'),Count('lost__id'))

        scores = []
        ranking = {}

        for index, record in enumerate(records_by_id):
            spread = record['won__id__count'] ** 2 - record['lost__id__count'] ** 2
            records_by_id[index]['spread'] = spread if spread > 0 else 0

            scores.append(records_by_id[index]['spread'])

        scores = sorted(scores)[-10:] # Keep only highest ten scores
        scores.reverse()

        for record in records_by_id:

            if record['spread'] in scores:
                record['artwork'] = vars(Artwork.objects.get(id=record['id']))
                ranking[scores.index(record['spread']) + 1] = record
                scores[scores.index(record['spread'])] = None # This spot is no longer available

        plays = Vote.objects.count()
        unique_artworks = Artwork.objects.count()

        context = {
            'ranking': ranking,
            'display_fields': display_fields,
            'plays': plays,
            'uniques': unique_artworks,
        }

        return render(request, self.template_name, context)

class MashNoVotesView(TemplateView):

    template_name = 'mash/novotes.html'

    def get(self, request, **kwargs):

        import random

        no_votes = Artwork.objects.all().exclude(won__id__isnull=False).exclude(lost__id__isnull=False)
        sample_no_votes = random.sample(no_votes, 6 if no_votes.count() >= 6 else no_votes.count())

        context = {
            'total': no_votes.count(),
            'artwork': sample_no_votes,
        }

        return render(request, self.template_name, context)

class UnlockedView(TemplateView):

    template_name = 'mash/unlocked.html'

    def get(self, request, **kwargs):

        context = {}

        from apps.mash.available_apis import available_apis as apis

        for api_code, api_info in apis.items():

            print api_code, api_info

            if api_code == 'luce':
                context[api_code] = {
                    'name': 'Smithsonian American Art Museum Luce Center',
                    'from_api': 'luce',
                }
            elif api_code == 'brooklyn':
                context[api_code] = {
                    'name': 'Brooklyn Museum',
                    'from_api': 'brooklyn',
                }
            elif api_code == 'victoriaalbertmuseum':
                context[api_code] = {
                    'name': 'Victoria and Albert Museum',
                    'from_api': 'Victoria and Albert Museum',
                }
            elif api_code == 'waltersmuseum':
                context[api_code] = {
                    'name': 'Walters Museum',
                    'from_api': 'Walters Museum',
                }

            context[api_code]['valuemin'] = 0
            context[api_code]['valuemax'] = api_info[1]
            context[api_code]['progress'] = Artwork.objects.filter(from_api=context[api_code]['from_api']).count()

            context[api_code]['current'] = (float(context[api_code]['progress']) / float(context[api_code]['valuemax'])) * 100

            # Color progression of the progress bars
            if context[api_code]['current'] <= 20:
                context[api_code]['color'] = 'progress-bar-danger'
                if context[api_code]['current'] <= 1:
                    context[api_code]['current'] = 1
            elif context[api_code]['current'] <= 40:
                context[api_code]['color'] = 'progress-bar-warning'
            elif context[api_code]['current'] <= 60:
                context[api_code]['color'] = 'progress-bar-info'
            elif context[api_code]['current'] <= 80:
                context[api_code]['color'] = 'progress-bar'
            else:
                context[api_code]['color'] = 'progress-bar-success'

        context = {
            'apis': context
        }

        return render(request, self.template_name, context)

class MashRankingView(TemplateView):

    template_name = 'mash/ranking.html'

    def get(self, request, **kwargs):

        context = self.get_context_data()
        print context

        return render(request, self.template_name, context)

    @staticmethod
    def get_children(ranking, identifier, mashups, wins=True):

        """
            Assumes wins are on the left side, losses on the right side.
        """

        if wins:
            position = 0
            opposite = 1
            level = 'above'
        else:
            position = 1
            opposite = 0
            level = 'below'

        current_length = len(ranking[identifier][level])

        for mashup in mashups:
            if mashup[position] == identifier:
                ranking[identifier][level].append(mashup[opposite])

            if mashup[position] in ranking[identifier][level]:
                ranking[identifier][level].append(mashup[opposite])

        ranking[identifier][level] = list(set(ranking[identifier][level]))

        if len(ranking[identifier][level]) != current_length:
            ranking[identifier] = MashRankingView.get_children(ranking, identifier, mashups, wins)

        return ranking[identifier]

    def get_context_data(self, **kwargs):

        mashups = []
        all_ids = []

        votes = Vote.objects.all()

        for vote in votes:
            mashups.append((vote.won_id, vote.lost_id))
            all_ids.extend([vote.won_id, vote.lost_id])

        all_ids = list(set(all_ids))

        # DO NOT USE .fromkeys() to build this dictionary!
        # If you do, all of the 'above' lists and 'below' lists will have the same IDs
        # Which means that appending to one 'above' list appends to EVERY 'above' list.
        # Using a dictionary comprehension will instantiate a new list for each one_id
        ranking = {one_id: {'above': [], 'below': []} for one_id in all_ids}

        for key in ranking.iterkeys():
            ranking[key] = self.get_children(ranking, key, mashups)
            ranking[key] = self.get_children(ranking, key, mashups, False)

        high_score = [0, 0] # score, id

        for key,value in ranking.iteritems():
            if (len(value['above']) - len(value['below'])) > high_score[0]:
                clear_winner = True

                high_score = [(len(value['above']) - len(value['below'])), key]
                wins = len(value['above'])
                losses = len(value['below'])
                above = value['above']
                below = value['below']
            elif (len(value['above']) - len(value['below'])) == high_score[0]:
                clear_winner = False

        plays = Vote.objects.count()
        uniques = Artwork.objects.count()

        rank = {
            'score': high_score[0],
            'art': Artwork.objects.get(id=high_score[1]),

            'wins': wins,
            'losses': losses,
            'above': above,
            'clear_winner': clear_winner,

            'plays': plays,
            'uniques': uniques,
        }

        return rank