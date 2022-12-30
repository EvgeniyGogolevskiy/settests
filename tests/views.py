from django.shortcuts import render
from django.views import generic
from .models import SetTests, NameTest, Question, CountAnswer


def index(request):
    settests = SetTests.objects.all()
    nametests = [{'title': s.title, 'tests': NameTest.objects.filter(settest=s)} for s in settests]
    return render(request, 'tests/index.html',
                  {'title': 'Главная страница сайта', 'nametests': nametests})


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
            calc_answer = calculateAnswer(resultAnswer[:-1])
            data = {'result': calc_answer[0], 'percent': calc_answer[1]}

            nametest = NameTest.objects.get(slug=self.kwargs.get('slug'))
            try:
                answer_get = CountAnswer.objects.get(nametest=nametest)
                answer_get.results = calc_answer[2]
                answer_get.save()
            except Exception:
                user_answer = CountAnswer(user=request.user, nametest=nametest, results=calc_answer[2])
                user_answer.save()

            return render(request, 'tests/finish_test.html', context=data)
        return super().get(request, *args, **kwargs)


def calculateAnswer(resultAnswer):
    list = resultAnswer.split(',')
    count = list.count('True')
    result = f"Количество правильных ответов: {count} из {len(list)}"
    percent = f"Процент правильных ответов: {round(count*100/len(list),2)}"
    return result, percent, count
