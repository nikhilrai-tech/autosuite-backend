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
                "__Secure-1PSID": "cwiNajKeMxHBXZcGFAcuhwW5lMFOY6b2O1ESQfQgXT507cg7kJ5q0wjKwQjttZXZQIveOw.",
                "__Secure-1PSIDTS": "sidts-CjIBNiGH7tpqeqD0ceIXw8cIhuf6jDOdJSU5_FhVc5-LBR1EjPM-vkgo2k6ysPUgwjeZ9hAA",
                "__Secure-1PSIDCC": "ACA-OxNehDFKHvY8Lu-SpuDZHt8P781nCL7rI1J8MsNytd4qMZYTVVE5_pJio63LzHq2RNMeNsY"
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
    def get(self, request, format=None):
        last_five_requests = BardRequest.objects.order_by('-id')[:1]
        data_to_return = [
            {'question': req.question, 'answer': BardResponse.objects.get(request=req).answer}
            for req in last_five_requests
        ]
        return Response(data_to_return, status=status.HTTP_200_OK)
    
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

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from selenium import webdriver
chrome_options = webdriver.ChromeOptions() 

# Path to your chrome binary 
chrome_binary = r"C:/Users/Nikhil Rai/Downloads/chromedriver-win64/chromedriver.exe"

chrome_options.binary_location = chrome_binary

# Create new instance of chromedriver using the chrome binary path
class CropSeedPriceView(APIView):

    def post(self, request):

        crop_name = request.data.get('crop_name')
        if not crop_name:
            return JsonResponse({'error':'Please provide a crop name.'}, status=400)

        driver = webdriver.Chrome(options=chrome_options)

        urls = [
            'https://agribegri.com/seeds/pulses-seeds-buy-online.php',
            'https://seed2plant.in/collections/seeds?utm_medium=cpc&utm_source=google&utm_campaign=SmartShoppingSeeds&gad_source=1&gclid=CjwKCAjwvrOpBhBdEiwAR58-3AN57ZLjGnucR_BDfxt_cl2KcgyrApCia8ajp1cpSIRVVymtIYuK9hoCDNsQAvD_BwE'
        ]
        
        price_results = []

        for url in urls:

            driver.get(url)

            # Fill crop name in search box 
            search_box = driver.find_element(By.ID, "search_product")
            search_box.clear()
            search_box.send_keys(crop_name)
            search_box.send_keys(Keys.RETURN)

            # Wait for results to load
            time.sleep(5)

            # Parse page source
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')

            # Find price element
            price_element = soup.find("div", {"class":"product-price"})
            
            if price_element:
                price = price_element.text.strip()
                price_results.append({url: price})

        driver.quit()
        
        if not price_results:
            return JsonResponse({'error': f'No prices found for "{crop_name}"'}, status=404) 

        return JsonResponse(price_results, safe=False)