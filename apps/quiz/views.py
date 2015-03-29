from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from apps.mash.models import Artwork, Vote
from apps.quiz.models import HighScore

class QuizChoiceView(TemplateView):

    " Display choices of available quiz types "
    
    template_name = 'quiz/quiz_choice.html'

    def get(self, request, **kwargs):

        """ Set session to no quiz type.
        """

        try:
            del request.session['quiz_type']
        except KeyError:
            pass

        try:
            del request.session['questions_missed']
        except KeyError:
            pass

        try:
            del request.session['question_number']
        except KeyError:
            pass

        try:
            del request.session['score']
        except KeyError:
            pass

        context = {}
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):

        """ Set session with which quiz type to play.
        """

        quiz_type = request.POST.get('quiz_type')
        if quiz_type in ('Q20','Miss3'):
            request.session['quiz_type'] = quiz_type
        else:
            request.session['quiz_type'] = 'Q20'
        return HttpResponseRedirect('/art/quiz')

class QuizHighScoreView(TemplateView):

    template_name = 'quiz/highscore.html'

    def get(self, request, **kwargs):

        """ View the high scores!
        """

        kwargs['quiz_type'] = request.session.get('quiz_type', 'Q20')

        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):

        """ Set a high score! You've earned it :)
        """

        quiz_type = request.session.get('quiz_type', 'Q20')
        score = request.session.get('score', 0)
        name = request.POST.get('highscore_name', '')

        name = name.strip()
        if not name:
            name = 'AAA'

        try:
            score = int(score)
        except Exception:
            pass
        else:
            if score and name and quiz_type:
                request.session['player_name'] = name
                if quiz_type in ('Miss3', 'Q20'):
                    new_highscore = HighScore(**{
                        'quiz_type': quiz_type,
                        'score': score,
                        'name': name
                        })
                    new_highscore.save()

        kwargs['quiz_type'] = quiz_type
        request.session['score'] = 0

        return HttpResponseRedirect('/art/highscore')

    def get_context_data(self, **kwargs):

        quiz_type = kwargs.get('quiz_type', 'Q20')

        highscores = HighScore.objects.filter(**{
            'quiz_type': quiz_type
            }).order_by('-score')[:10]

        context = {
            'highscores': highscores,
            'quiz_type': quiz_type
        }

        return context

class QuizView(TemplateView):

    template_name = 'quiz/quiz.html'

    def get(self, request, **kwargs):

        " Initial state of the quiz "

        context = self.get_context_data(**kwargs)

        if not request.session.get('question_number'):
            request.session['question_number'] = 1

        if not request.session.get('quiz_type'):
            request.session['quiz_type'] = 'Q20'

        if not request.session.get('questions_missed'):
            request.session['questions_missed'] = 0

        if request.session.get('game_over'):
            if request.session.get('quiz_type') in ('Q20', 'Miss3'):
                request.session['score'] = request.session['question_number'] - request.session['questions_missed'] - 1
            request.session['question_number'] = 1
            request.session['questions_missed'] = 0
            request.session['game_over'] = False

        context["question_number"] = request.session.get('question_number')
        context["quiz_type"] = request.session.get('quiz_type')
        context['questions_missed'] = request.session.get('questions_missed')
        context['game_over'] = request.session.get('game_over')

        return render(request, self.template_name, context)

    def post(self, request, **kwargs):

        " Quiz state after at least one question has been answered"

        previous_artwork = request.POST.get('artwork_id')
        question = request.POST.get('question')
        answer = request.POST.get('artwork_{0}'.format(question))

        if not request.session['question_number']:
            request.session['question_number'] = 0

        request.session['question_number'] += 1

        context = self.get_context_data(**kwargs)

        try:
            previous_artwork = Artwork.objects.get(id=previous_artwork)
        except Exception:
            pass
        else:
            correct_answer = vars(previous_artwork)[question]

            if vars(previous_artwork)[question] == answer:
                context["correct"] = True
            else:
                context["correct"] = False
                request.session['questions_missed'] += 1

            context["previous_artwork"] = previous_artwork.id
            context["question_was"] = question
            context["answered_as"] = answer
            context["correct_answer"] = correct_answer
            context["post"] = True

            context["question_number"] = request.session['question_number']

        # In game type Q20, you get 20 quiz questions to answer
        if request.session['quiz_type'] == 'Q20' and request.session['question_number'] > 20:
            request.session['game_over'] = True
            context["game_over"] = True
        # In game type Miss3, you go until you get 3 wrong
        elif request.session['quiz_type'] == 'Miss3' and request.session['questions_missed'] > 2:
            request.session['game_over'] = True
            context["game_over"] = True 

        context['quiz_type'] = request.session["quiz_type"]
        context['questions_missed'] = request.session['questions_missed']

        if context.get("game_over"):
            context["question_number"] -= 1
            context["questions_correct"] = context["question_number"] - context['questions_missed']
            context["player_name"] = request.session.get('player_name', "")
            request.session['score'] = context["questions_correct"]

        return render(request, self.template_name, context)        

    def get_context_data(self, **kwargs):

        " Get one quiz question "

        import random

        question_types = (
            'title',
            'artist',
            'date',
        )

        # Some quiz clues aren't helpful. 
        # Example: 'Untitled' is a bad title that doesn't make it easy to guess.
        # Add new items here to filter out artworks that match these.
        bad_quiz_clues = {
            'title': ('', 'untitled', 'none'),
            'artist': ('', 'unknown', 'anonymous', 'none'),
            'date': ('', 'unknown', 'none', 'n.d.'),
        }

        game_type = kwargs.get('game_type')
        if game_type == 'quiz':
            kwargs['choices'] = 4
            kwargs['decoys'] = 3
        elif game_type == 'twotruthsonelie':
            kwargs['choices'] = 3
            kwargs['decoys'] = 1
        else:
            # Default to quiz
            kwargs['choices'] = 4
            kwargs['decoys'] = 3

        question_type = random.choice(question_types)

        artwork = Artwork.objects.get(id=random.randint(1, Artwork.objects.count() - 1))

        while unicode(vars(artwork)[question_type]).strip().lower() in bad_quiz_clues[question_type]:
            artwork = Artwork.objects.get(id=random.randint(1, Artwork.objects.count() - 1))

        choices = kwargs.get('choices')
        decoys = kwargs.get('decoys')

        context = {"decoy{0}".format(x): artwork for x in range(decoys)}
        context['artwork'] = artwork
        context['question'] = question_type

        used = [artwork.id]
        context['clues'] = list()
        context['clues'].append(artwork)

        for index in range(decoys):
            while context['decoy{0}'.format(index)] == artwork:
                new_artwork = random.randint(1, Artwork.objects.count() - 1)
                
                # Ensure that no two decoys are the same
                if new_artwork in used:
                    context['decoy{0}'.format(index)] = artwork

                context['decoy{0}'.format(index)] = Artwork.objects.get(id=new_artwork)

                # If any of the chosen artworks have bad quiz clues, get another
                if unicode(vars(context['decoy{0}'.format(index)])[question_type]).strip().lower() in bad_quiz_clues[question_type]:
                    context['decoy{0}'.format(index)] = artwork
                else:
                    used.append(new_artwork)
                    context['clues'].append(context['decoy{0}'.format(index)])

        random.shuffle(context['clues'])

        return context