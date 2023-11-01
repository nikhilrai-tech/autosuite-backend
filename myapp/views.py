from django.http import JsonResponse
from bardapi import BardCookies
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import BardRequest, BardResponse
# class BardAnswerView(APIView):
#     def post(self, request, format=None):
#         question = request.data.get('question')
#         if question:
#             cookie_dict = {
#                 "__Secure-1PSID": "bgiNas0Ggj5jT103CiGbi0rIJ-YkLt-z0ricoqkLn7HucnSvPl2bv65nw2lM7lLT04slbA.",
#                 "__Secure-1PSIDTS": "sidts-CjIBNiGH7l2GdkvzvwXE9lLFgqWIJ4BtVhq6yeg74AFML3KYwKKHsJSPKAlHLRkvL33xgRAA",
#                 "__Secure-1PSIDCC": "ACA-OxNV810ZcpcuPJxhmcjGjCGm6m0_On9jYeSJh8GR0kpUxK-FoNjv-_722izSdaC94y5cCa4"
#             }
#             bard = BardCookies(cookie_dict=cookie_dict)
#             reply = bard.get_answer(question)['content']
#             request_instance = BardRequest(question=question)
#             request_instance.save()
#             response_instance = BardResponse(request=request_instance, answer=reply)
#             response_instance.save()
#             return Response({'answer': reply}, status=status.HTTP_200_OK)
#         return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
import requests
class BardAnswerView(APIView):
    def post(self, request, format=None):
        question = request.data.get('question')
        if question:
            cookie_dict = {
                "__Secure-1PSID": "bgiNas0Ggj5jT103CiGbi0rIJ-YkLt-z0ricoqkLn7HucnSvPl2bv65nw2lM7lLT04slbA.",
                "__Secure-1PSIDTS": "sidts-CjIBNiGH7l2GdkvzvwXE9lLFgqWIJ4BtVhq6yeg74AFML3KYwKKHsJSPKAlHLRkvL33xgRAA",
                "__Secure-1PSIDCC": "ACA-OxNV810ZcpcuPJxhmcjGjCGm6m0_On9jYeSJh8GR0kpUxK-FoNjv-_722izSdaC94y5cCa4"
            }
            bard = BardCookies(cookie_dict=cookie_dict, timeout=30)
            try:
                reply = bard.get_answer(question)['content']
                request_instance = BardRequest(question=question)
                request_instance.save()
                response_instance = BardResponse(request=request_instance, answer=reply)
                response_instance.save()
                return Response({'answer': reply}, status=status.HTTP_200_OK)
            except requests.exceptions.ReadTimeout as e:
                return Response({'error': f'Request timed out after 30 seconds: {e}'}, status=status.HTTP_504_GATEWAY_TIMEOUT)
        return Response({'error': 'Invalid request'}, status=status.HTTP_400_BAD_REQUEST)
    
from . serializers import BardResponseSerializer,BardRequestSerializer

class BardResponseUpdateView(UpdateAPIView):
    queryset = BardRequest.objects.all()
    serializer_class = BardRequestSerializer
from rest_framework.generics import CreateAPIView
class BardRequestCreateView(CreateAPIView):
    queryset = BardRequest.objects.all()
    serializer_class = BardRequestSerializer
    def create(self, request, *args, **kwargs):
        default_question = BardRequest.objects.first()
        if default_question:
            cookie_dict = {
                "__Secure-1PSID": "bgiNas0Ggj5jT103CiGbi0rIJ-YkLt-z0ricoqkLn7HucnSvPl2bv65nw2lM7lLT04slbA.",
                "__Secure-1PSIDTS": "sidts-CjIBNiGH7j1S3jlPRGX0prepKiMwG1C1HzJUY8psQJGxAyjYDX7V1ldV3up7dNLw3dD4MxAA",
                "__Secure-1PSIDCC": "ACA-OxN2zxPB8olMWhpQRqcOFBNjQLObgElpIJwG1XZT6occIg4PbGNI5OZiU-LyI5skDOL_8ow"
            }
            bard = BardCookies(cookie_dict=cookie_dict, timeout=30)
            try:
                reply = bard.get_answer(default_question.question)['content']
                serializer = self.get_serializer(data={'question': default_question.question, 'answer': reply})
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
            except requests.exceptions.ReadTimeout as e:
                return Response({'error': f'Request timed out after 30 seconds: {e}'}, status=status.HTTP_504_GATEWAY_TIMEOUT)  
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({'error': 'No default question found'}, status=status.HTTP_400_BAD_REQUEST)