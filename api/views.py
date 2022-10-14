from rest_framework.response import Response
from rest_framework.decorators import api_view
from answerss.questiontwo import api_call


@api_view(['post'])
def regex_to_nfa(request):
    person = {"Question": "1"}
    return Response(person)


@api_view(['post'])
def nfa_to_dfa(request):

    return Response(api_call(request.body))


@api_view(['post'])
def regex_to_dfa(request):
    person = {"Question": "3"}
    return Response(person)
