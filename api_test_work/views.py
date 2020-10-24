from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .tasks import parse_task, checking_task


class StartParser(APIView):

    def get(self, request):
        parse_task.delay() # start parser
        return Response({"Success": "parser started"}, status=status.HTTP_200_OK)


class StartCheck(APIView):

    def get(self, request):
        checking_task.delay()
        return Response({"Success": "cheking started"}, status=status.HTTP_200_OK)
