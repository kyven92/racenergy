from rest_framework import serializers


from racIOT.models import RPS_Data


class RPSDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=RPS_Data
        fields=('student_name','entry_id','year_of_birth','gender','height','weight','nationality','course','last_score','ailments')