from django.urls import path
from . import views


urlpatterns = [
    path('regex-nfa/', views.regex_to_nfa),
    path('nfa-dfa/', views.nfa_to_dfa),
    path('regex-dfa/', views.regex_to_dfa),
]
