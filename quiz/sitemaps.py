from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from django.core.paginator import Paginator
from .models import Class, Quiz, Poll, StudentQuizInfo

class ClasSitemap(Sitemap) :
    def items(self):
        return Class.objects.all()

class QuizSitemap(Sitemap):
    def items(self):
        return Quiz.objects.filter(make_visible=True)

class PollSitemap(Sitemap):
    def items(self):
        return Poll.objects.filter(activate=True)

class QuizResultSitemap(Sitemap):
    def items(self):
        return StudentQuizInfo.objects.all()

class StaticHomeSitemap(Sitemap):
    def items(self):
        return ['quiz:home']

    def location(self, item):
            return reverse(item)