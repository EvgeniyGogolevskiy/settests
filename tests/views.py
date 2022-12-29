import eel as eel
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import generic
from .models import SetTests, NameTest, Question, Answer


def index(request):
    settests = SetTests.objects.all()
    nametests = [{'title': s.title, 'tests': NameTest.objects.filter(settest=s)} for s in settests]
    return render(request, 'tests/index.html',
                  {'title': 'Главная страница сайта', 'settests': settests, 'nametests': nametests})


class QuestionView(generic.ListView):
    model = Question
    template_name = 'tests/question.html'
    paginate_by = 1

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        qs = Question.objects.filter(nametest__slug=slug)
        return qs

    def get(self, request, *args, **kwargs):
        resultAnswer = self.request.GET.get("btn_test")
        if resultAnswer:
            data = {'result': calculateAnswer(resultAnswer[:-1])}
            return render(request, 'tests/finish_test.html', context=data)
        return super().get(request, *args, **kwargs)


def calculateAnswer(resultAnswer):
    list = resultAnswer.split(',')
    count = list.count('True')
    result = f"Количество правильных ответов: {count} из {len(list)}"
    return result
