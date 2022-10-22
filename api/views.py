from rest_framework.response import Response
from rest_framework.decorators import api_view
from answerss.questiontwo import api_call
from answerss.Regextonfa import api_call
from answerss.questionthree import regexToDFA


@api_view(["post"])
def regex_to_nfa(request):
    return Response(api_call(request.body))


@api_view(["post"])
def nfa_to_dfa(request):

    return Response(api_call(request.body))


@api_view(["post"])
def regex_to_dfa(request):

    return Response(regexToDFA(request.body))
