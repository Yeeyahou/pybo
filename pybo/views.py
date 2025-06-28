from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer
from django.shortcuts import render
from .forms import ScraperForm
from .models import ScrapedData
import requests
from bs4 import BeautifulSoup


def scraper_view(request):
    if request.method == 'POST':
        form = ScraperForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            tag = form.cleaned_data['tag']
            class_name = form.cleaned_data['class_name']

            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')

                if class_name:
                    elements = soup.find_all(tag, class_=class_name)
                else:
                    elements = soup.find_all(tag)

                content = '\n'.join([elem.text.strip() for elem in elements])

                # 스크랩한 데이터 저장
                scraped_data = ScrapedData.objects.create(
                    url=url,
                    tag=tag,
                    class_name=class_name,
                    content=content
                )

                return render(request, 'pybo/scraper.html', {
                    'form': form,
                    'content': content,
                    'success': True
                })

            except Exception as e:
                return render(request, 'pybo/scraper.html', {
                    'form': form,
                    'error': str(e)
                })
    else:
        form = ScraperForm()

    return render(request, 'pybo/scraper.html', {'form': form})

def index(request):
    question_list = Question.objects.order_by('-create_date')
    context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)

def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(content=request.POST.get('content'), create_date=timezone.now())
    return redirect('pybo:detail', question_id=question.id)

# API 뷰
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def perform_destroy(self, instance):
        instance.soft_delete()

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        question = self.get_object()
        question.restore()
        serializer = self.get_serializer(question)
        return Response(serializer.data)

class AnswerViewSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

    def perform_destroy(self, instance):
        instance.soft_delete()

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        answer = self.get_object()
        answer.restore()
        serializer = self.get_serializer(answer)
        return Response(serializer.data)