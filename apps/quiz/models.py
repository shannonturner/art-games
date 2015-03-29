from django.db import models


class HighScore(models.Model):
    quiz_type = models.CharField(max_length=255, default="Q20")
    name = models.CharField(max_length=255, blank=True)
    score = models.IntegerField(default=0)

    def __unicode__(self):
        return "{0} ({1})".format(self.score, self.name)
