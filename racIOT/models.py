from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


# Create your models here.

class User(AbstractUser):
    rps_id=models.IntegerField(unique=True,default=1)
    created=models.DateField(auto_now_add=True)

    @staticmethod
    def create_user(**kwargs):
        user = User(**kwargs)
        user.clean()
        user.save()
        return user


    def name(self):
        return str(self.first_name + " " + self.last_name).strip()


    def __str__(self):
        return str(self.name() or self.id.__str__())



class RPS_Data(models.Model):
    user_fk=models.ForeignKey(User,blank=True,null=True,on_delete=models.SET_NULL, related_name="RPS_User")
    student_name=models.CharField(max_length=100, blank=True, null=True)
    entry_id=models.IntegerField(db_index=True,default=-1)
    year_of_birth=models.IntegerField(default=None,blank=True,null=True)
    gender=models.CharField(max_length=20, blank=True, null=True)
    height=models.FloatField(blank=True,null=True)
    weight=models.FloatField(blank=True,null=True)
    nationality=models.CharField(max_length=100, blank=True, null=True)
    course=models.CharField(max_length=100, blank=True, null=True)
    last_score=models.FloatField(blank=True,null=True)
    ailments=models.BooleanField(default=False)

    class Meta:
        unique_together=('user_fk','entry_id')

    def __str__(self):
        return str(self.entry_id)
