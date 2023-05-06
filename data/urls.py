from django.urls import path,include
from . import views
from .router import router

urlpatterns = [
    path('', include(router.urls)),
    path('calc', views.CalcTest.as_view()),
    path('calc_result', views.CalcTestResult.as_view()),
]
