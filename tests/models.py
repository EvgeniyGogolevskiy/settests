import textwrap

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

from .querysets import AnswerQuerySet


class SetTests(models.Model):
    slug = models.SlugField('Ссылка на тему')
    title = models.CharField('Тема', max_length=100)

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'

    def __str__(self):
        return self.title


class NameTest(models.Model):
    settest = models.ForeignKey(SetTests, verbose_name='Тема набора тестов', on_delete=models.CASCADE, related_name='nametest')
    slug = models.SlugField('Ссылка на тест')
    title = models.CharField('Тест', max_length=100)
    description = models.TextField('Описание', blank=True, null=True)
    is_active = models.BooleanField('Доступ', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'
        ordering = ['created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('question', kwargs={'slug': self.slug})


class Question(models.Model):
    nametest = models.ForeignKey(NameTest, verbose_name='Тест', on_delete=models.CASCADE, related_name='question')
    text = models.TextField('Текст')
    order = models.PositiveSmallIntegerField('Order', default=0)

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['id']

    def __str__(self):
        return textwrap.shorten(self.text, width=50, placeholder="...")

    def get_absolute_url(self):
        return reverse('question', kwargs={'int': self.order})


class Answer(models.Model):
    question = models.ForeignKey(Question, verbose_name='Вопрос', on_delete=models.CASCADE, related_name='answer')
    text = models.CharField('Текст', max_length=255)
    is_valid = models.BooleanField('Правильность', default=False)

    objects = AnswerQuerySet.as_manager()

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return textwrap.shorten(self.text, width=50, placeholder="...")


class CountAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nametest = models.ForeignKey(NameTest, on_delete=models.CASCADE)
    results = models.CharField('Результат', max_length=255)

    def __str__(self):
        return f'{self.nametest} - {self.results} верных ответа'