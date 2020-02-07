from django.shortcuts import render
from django.http import HttpResponse,HttpRequest

from django.views.generic import View
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Avg



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated  

from rest_framework.authtoken.models import Token

from racIOT.serializers import RPSDataSerializer
from racIOT.models import User,RPS_Data

import json


# Create your views here.


class helloView(APIView):
    permission_classes = (IsAuthenticated,)


    def get(self,request):
        # print("####################")

        content = {'message':'Hello'}
        return Response(content)



class uploadRPSData(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        print("Request Body: ", request.data)
        print("Request Authorization: ", request.headers['Authorization'])
        auth_token = request.headers['Authorization'].rstrip().split()[1]
        print("Response Token: ",request.headers['Authorization'].rstrip().split()[1])
        user_id_t=Token.objects.values_list('user_id',flat=True).get(key=auth_token)
        print("User ID: ",user_id_t)

        for json_obj in request.data:

            RPS_User=User.objects.get(id=user_id_t)
            serializer=RPSDataSerializer(data=json_obj)
            serializer.is_valid(raise_exception=True)
            serializer.save(user_fk=RPS_User)

        return_json = {'status':"success"}


        return HttpResponse(json.dumps(return_json))


class getLatestEmtry(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        auth_token = request.headers['Authorization'].rstrip().split()[1]
        user_id_t=Token.objects.values_list('user_id',flat=True).get(key=auth_token)

        RPS_User=User.objects.get(id=user_id_t)
        last_entry_id=RPS_Data.objects.values_list('entry_id',flat=True).filter(user_fk=RPS_User).last()
        if last_entry_id is None:
            last_entry_id=0
            print("Last Entry ID: ",last_entry_id)
        return_json = {'last_entry':last_entry_id}

        return HttpResponse(json.dumps(return_json))


class HomePageView(LoginRequiredMixin,View):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # print("#############: Authenticated")
            return render(request, 'charts.html')
        else:
            # print("#############: Redirecting")
            return HttpResponseRedirect('/login.html')



class no_of_students(LoginRequiredMixin,APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = {
            "years": [],
            "no_of_students": [],
        }
        years=list(RPS_Data.objects.order_by().values_list('year_of_birth',flat=True).distinct())
        years.sort()
        no_of_students=[RPS_Data.objects.filter(year_of_birth=year).distinct().count() for year in years ]


        data['years']=years
        data['no_of_students']=no_of_students

        print("### Data; ",data)


        return Response(data)


class genderPercentage(LoginRequiredMixin,APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = {
            "genders": [],
            "gender_percentage": [],
            "gender_heights": [],
            "gender_weights":[]
        }
        genders=list(RPS_Data.objects.order_by().values_list('gender',flat=True).distinct())
        total_students = RPS_Data.objects.order_by().values_list('student_name',flat=True).distinct().count()
        gender_percentage=[(RPS_Data.objects.filter(gender=gender).distinct().count()/total_students)*100 for gender in genders ]
        gender_heights=[RPS_Data.objects.filter(gender=gender).distinct().aggregate(Avg('height'))['height__avg'] for gender in genders ]
        gender_weights=[RPS_Data.objects.filter(gender=gender).distinct().aggregate(Avg('weight'))['weight__avg'] for gender in genders ]

        data['genders']=genders
        data['gender_percentage']=gender_percentage
        data['gender_heights']=gender_heights
        data['gender_weights']=gender_weights


        print("### Data; ",data)
        return Response(data)


class genderAilments(APIView):
    # permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        data = {
            "ailments": [],
            "ailments_percentages": [],
            "male_ailments":[],
            "female_ailments":[]

        }
        ailments=list(RPS_Data.objects.order_by().values_list('ailments',flat=True).distinct())
        total_students = RPS_Data.objects.order_by().values_list('student_name',flat=True).distinct().count()
        # ailments_percentages=[(RPS_Data.objects.filter(ailments=ailment).distinct().count()/total_students)*100 for ailment in ailments ]
        ailments_percentages=[RPS_Data.objects.filter(ailments=ailment).distinct().count() for ailment in ailments ]
        male_ailments=[RPS_Data.objects.filter(gender='Male',ailments=ailment).distinct().count() for ailment in ailments]
        female_ailments=[RPS_Data.objects.filter(gender='Female',ailments=ailment).distinct().count() for ailment in ailments ]

        data['ailments']=ailments
        data['ailments_percentages']=ailments_percentages
        data['male_ailments']=male_ailments
        data['female_ailments']=female_ailments


        # print("### Data; ",data)
        return Response(data)
