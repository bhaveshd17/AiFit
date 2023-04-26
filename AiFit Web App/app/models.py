from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from ckeditor.fields import RichTextField


class UserDetails(models.Model):
    username = models.OneToOneField(User,on_delete=CASCADE, null=True, blank=True)
    name = models.CharField(max_length=120, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=sorted({
        ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')
    }),  blank=True, null=True)
    age = models.CharField(max_length=5, blank=True, null=True)
    activity_level = models.CharField(max_length=200, choices=sorted({
        ('1','Sedentary'),('2','Lightly active'),('3','Moderatly active'),('4','Very active')
    }), blank=True, null=True)
    height = models.CharField(max_length=4, blank=True, null=True)
    weight = models.CharField(max_length=3, blank=True, null=True)
    main_goal=models.CharField(max_length=20, choices=sorted({
        ('1','Loose Weight'),('2','Build Muscels'),('3','Keep Fit')
    }), blank=True, null=True)
    medical_conditions = models.CharField(max_length=500, blank=True, null=True)
    

    def __str__(self):
        return str(self.username)
    

def video_collection_path(instance, filename):
    return f"recorded_videos/{filename}"

class Record(models.Model):
    username = models.ForeignKey(User, on_delete=CASCADE, null=True, blank=True)
    video = models.FileField(upload_to=video_collection_path)
    
    def __str__(self):
        return str(self.id)
 
 
class Trainer_form(models.Model):    
    title= models.CharField(max_length=100)
    # image= CloudinaryField('event')
    image=models.FileField(upload_to="Exercise Images/")
    f_area= models.TextField(max_length=100)
    equipment= models.TextField(max_length=100)
    prep= models.TextField(max_length=1000)
    execution= models.TextField(max_length=1000)
    keyTip= models.TextField(max_length=1000)

    def __str__(self):
        return self.title    
        
class Accuracy(models.Model):
    username = models.ForeignKey(User, on_delete=CASCADE, null=True, blank=True)
    exercise = models.ForeignKey(Trainer_form, on_delete=CASCADE, null=True, blank=True)
    avg_accuracy = models.CharField(max_length=40, null=True, blank=True)
    duration = models.CharField(max_length=40, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{str(self.username)} - {str(self.exercise.title)}"



class BlogModel(models.Model):
    title = models.CharField(max_length=1000)
    content = RichTextField(blank=True,null=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    view = models.IntegerField(null=True, blank=True, default=0) 
    link = models.CharField(max_length=1000,null=True)
    image=models.ImageField(upload_to="Blogs/Cover Images", null=True)
    
    

    def __str__(self):
        return self.title     

   
