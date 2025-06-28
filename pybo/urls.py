from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
app_name = 'pybo'

router = DefaultRouter()
router.register(r'questions', views.QuestionViewSet)
router.register(r'answers', views.AnswerViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('answer/create/<int:question_id>/', views.answer_create, name='answer_create'),
    path('', include(router.urls)),
    path('scraper/', views.scraper_view, name='scraper'),
]