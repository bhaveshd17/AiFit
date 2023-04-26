from django.shortcuts import render, redirect
from django.http.response import StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
import random
from app.camera import VideoCamera, VideoCameraRealTime, VideoCameraRepCounter
from app.model_detection import predict_single_action
from django.contrib.auth import authenticate, login, logout
from .models import Record, Accuracy, Trainer_form, BlogModel, UserDetails
from .forms import TrainingForm,BlogForm, UserDataForm
from .decorators import unauthenticated_user
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
import json, requests
import time
import os
from aifit.settings import MEDIA_ROOT, MEDIA_URL
from django.core.files.base import ContentFile
from collections import deque 
from django.contrib.auth.decorators import login_required
from datetime import datetime
from datetime import timedelta

def gen(camera):
    time.sleep(1.0)
    while camera.get_frame():
        frame = camera.get_frame()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@login_required(login_url='login')
def video_feed(request, *args, **kwargs):
    obj = Record.objects.filter(username=User.objects.filter(username=request.user.username).first()).first()
    if obj is not None:
        file_path = obj.video.path
    else:
        file_path = '' 
    return StreamingHttpResponse(gen(VideoCamera(file_path)),
            content_type='multipart/x-mixed-replace; boundary=frame')
    
def rtdGen(key, camera, check_class):
    print(check_class, 'in rtd')
    time.sleep(1.0)
    confidence = 0
    predicted_class = ''
    frames_queue = deque(maxlen = 25)
    while True:
        frame, frames_queue, predicted_class, confidence = camera.get_frame(key, frames_queue, predicted_class, confidence, check_class)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@login_required(login_url='login')         
def rtd_video_feed(request, *args, **kwargs):
    check_class = request.GET.get('check_class')
    key = request.GET.get('key')
    gen_obj = rtdGen(key, VideoCameraRealTime(), check_class)
    return StreamingHttpResponse(gen_obj,
            content_type='multipart/x-mixed-replace; boundary=frame')
    

def gen_rep(camera):
    time.sleep(1.0)
    counter = 0
    stage = None
    while True:
        frame, up_counter, up_stage = camera.get_frame(counter, stage)
        counter, stage = up_counter, up_stage
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@login_required(login_url='login')
def video_feed_rep(request, *args, **kwargs): 
    return StreamingHttpResponse(gen_rep(VideoCameraRepCounter()),
            content_type='multipart/x-mixed-replace; boundary=frame')

# def webcam_feed(request, *args, **kwargs):
#     pass


def home__page(request, *args, **kwargs):
    return render(request, 'landing_page/home.html')


@login_required(login_url='login')
def dashboard(request, *args, **kwargs):
    user = UserDetails.objects.filter(username=User.objects.get(username=request.user.username)).first()
    return render(request, 'dashboard/dashboard.html', context={'user':user})

@login_required(login_url='login')
def check_form(request, *args, **kwargs):
    objects=Trainer_form.objects.all()
    context={'objects':objects}
    return render(request, 'Real Time Detection/check_form.html', context)



@login_required(login_url='login')
def check_form_detection(request, category,*args, **kwargs):
    flag = request.GET.get('flag')
    timer = request.GET.get('timer')
    s_key = request.GET.get('key')
    pred_class, confidence, s_obj = None, None, None
    if flag is None:
        flag = ''
    if s_key is not None:
        s_obj = Session.objects.filter(pk=s_key).first()
        if s_obj is not None:
            data = s_obj.get_decoded()
            pred_class = data['pred_class']
            print(data['confidence'])
            confidence = float(data['confidence'])
        else:
            return redirect('check_form_detection', category=category)
    else:
        pass

    if flag == 'upload':
        print(confidence)
        if category.upper() != pred_class.upper():
            pred_class = 'Inaccurate Workout'
            confidence = str(random.randint(1, 10)*0.01)
        context = {
            'category':category[0].upper()+category[1:],
            'flag': flag,
            'pred_class':pred_class,
            'confidence':confidence,
            'timer':timer
        }
        s_obj.delete()
    else:
        acc_s = SessionStore()
        acc_s['accuracy'] = []
        acc_s['category'] = category
        acc_s.create()
        key = acc_s.session_key
        context = {
            'category':category[0].upper()+category[1:],
            'flag': flag,
            'timer':timer,
            'key':key
        }
        if s_obj:
            s_obj.delete()
    return render(request, 'Real Time Detection/check_form_detection.html', context)

@login_required(login_url='login')
def upload_video_detection(request, category, *args, **kwargs):
    if request.method == 'POST':
        user = request.user.first_name.lower() +'_'+request.user.last_name.lower()
        upload_file = request.FILES.get('uploaded_video')
        user_obj = User.objects.filter(username=request.user.username).first()
        record_obj = Record.objects.filter(username=user_obj).first()
        if upload_file is not None:
            if record_obj is not None:
                ext = record_obj.video.name.split('.')[-1]
                file_path = MEDIA_ROOT+'/recorded_videos/'+user+'.'+str(ext)
                os.remove(file_path)
                record_obj.video.save(user+'.'+str(ext), upload_file,save=False)
                record_obj.save()
            else:
                record_obj = Record()
                ext = str(upload_file).split('.')[-1]
                record_obj.video.save(user+'.'+ext, upload_file,save=False)
                record_obj.username = user_obj
                record_obj.save()
            result = predict_single_action(record_obj.video.path, 25)
            s = SessionStore()
            print(result['confidence'])
            s['pred_class'] = result['class']
            s['confidence'] = str(result['confidence'])
            s.create()
            category = category[0].upper()+category[1:]
            return redirect(f'/check_form/{category}?flag=upload&key={s.session_key}')
    return redirect('check_form_detection', category=category)
            
        # else:
        #     file_name = f'{user}.mp4'
        #     if record_obj is not None:
        #         file_path = MEDIA_ROOT+'/recorded_videos/'+file_name
        #         os.remove(file_path)
        #         record_obj.video.save(file_name, ContentFile(request.body), save=False)
        #         record_obj.save()
        #     else:
        #         record_obj = Record()
        #         record_obj.video.save(file_name, ContentFile(request.body),save=False)
        #         record_obj.username = user_obj
        #         record_obj.save()
        
        #     result = predict_single_action(record_obj.video.path, 20)
        #     s = SessionStore()
        #     s['pred_class'] = result['class']
        #     s['confidence'] = str(result['confidence'])
        #     s.create()
        #     category = category[0].upper()+category[1:]
            
        #     return JsonResponse({
        #         'category':category, 
        #         'flag':True,
        #         'key': s.session_key
        #     })


@login_required(login_url='login')
def rep_counter_biceps(request,*args,**kwargs):
    flag = request.GET.get('flag')
    context = {
        'flag':flag
    }
    return render(request, 'Rep Counter/repcounter.html', context)


@login_required(login_url='login')
def analysis__lookup(request, *args, **kwargs):
    key = request.GET.get('key')
    timer = request.GET.get('timer')
    select_category = request.GET.get('select_category')
    realtime_acc = {}
    cat_ls = ["Bicep Curl", "Overhead Press", "Shoulder Raise", "Squats"]
    if key is not None and timer is not None:
        s_obj = Session.objects.filter(session_key=key).first()
        data = s_obj.get_decoded()
        avg_accuracy = round(sum(data['accuracy'])/len(data['accuracy']), 2)
        Accuracy.objects.create(
            username=User.objects.get(id=request.user.id),
            exercise=Trainer_form.objects.get(title__icontains=data['category']),
            avg_accuracy=avg_accuracy,
            duration=timer
        )
        realtime_acc['accuracy'] = avg_accuracy
        realtime_acc['category'] = data['category']
        realtime_acc['duration'] = timer
    
    
    if select_category is not None:
        
        acc_obj = Accuracy.objects.filter(username=User.objects.get(id=request.user.id), exercise=Trainer_form.objects.get(title=cat_ls[int(select_category)]))
        accuracy_chart_data = {'avg_accuracy':[], 'date':[]}
        for i in acc_obj:
            accuracy_chart_data['avg_accuracy'].append(i.avg_accuracy)
            accuracy_chart_data['date'].append(i.date.strftime('%Y-%m-%d'))
        
        wk_ls = {}
        acc_ojects = Accuracy.objects.filter(username=User.objects.get(id=request.user.id))
        for i in acc_ojects:
            key_elem = "".join(i.exercise.title.lower().split(' '))
            if key_elem not in wk_ls.keys():
                wk_ls[key_elem] = []
                wk_ls[key_elem].append(i.avg_accuracy)
            else:
                wk_ls[key_elem].append(i.avg_accuracy)
    else:
        return redirect('dashboard')
    context = {'realtime_acc':realtime_acc, 'accuracy_chart_data':accuracy_chart_data, 'wk_ls':wk_ls, 'select_category':cat_ls[int(select_category)], 'select_index':select_category}
    return render(request, 'Analysis/analysis.html', context=context)

@login_required(login_url='login')
def user_data(request):
    usr_form = UserDataForm()
    user_details = UserDetails.objects.filter(username=User.objects.get(username=request.user.username)).first()
    if user_details.name:
        return redirect('dashboard')
    if request.method == 'POST':
        usr_form = UserDataForm(request.POST)
        if usr_form.is_valid():
            usr = User.objects.get(username=request.user.username)
            user_detail_obj = UserDetails.objects.filter(username=usr)
            if user_detail_obj.first() is not None:
                print(usr_form.cleaned_data)
                user_detail_obj.update(**usr_form.cleaned_data)
                return redirect('dashboard')
            else:
                return redirect('userData')
        else:
            print(usr_form.errors)   
            return redirect('userData')
    content = {'usr_form':usr_form}
    return render(request, 'authentication/user_details.html', content)

@login_required(login_url='login')
def profile__lookup(request, id,*args, **kwargs):
    user = UserDetails.objects.filter(id=id).first()
    if user:
        context = {
            'user':user
        }
        return render(request, 'dashboard/profile.html', context=context)
    else:
        return redirect(dashboard)

@unauthenticated_user
def sign_up__lookup(request, *args, **kwargs):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')
        if password != cpassword:
            messages.error(request, 'Both the password should be same')
            return redirect(sign_up__lookup)
        
        user = User.objects.filter(username=username).first()
        if user is None:
            user = User.objects.create(username=username, email=username)
            user.set_password(password)
            user.save()
            
            UserDetails.objects.create(
                username=user
            )
            login(request, user)
            request.session.set_expiry(60 * 60 * 24)
            return redirect(user_data)
        else:
            messages.error(request, 'User already exist')
            return redirect(sign_up__lookup)
    return render(request, 'authentication/signup.html', context=context)

@unauthenticated_user
def login__lookup(request, *args, **kwargs):
    context={}
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session.set_expiry(60 * 60 * 24)
            return redirect(dashboard)
        else:
            messages.error(request, 'Incorrect user or Password')
            return redirect(login__lookup)
        
    return render(request, 'authentication/login.html', context=context)

def logout__lookup(request, *args, **kwargs):
    logout(request)
    return redirect(login__lookup)




#training website
@login_required(login_url='login')
def train(request,pk):
    context = {}
    try:
        object = Trainer_form.objects.filter(id=pk).first()
        # obj.save()
        context['object'] = object
    except Exception as e:
        print(e)
    return render(request,'training/training.html',context) 

@login_required(login_url='login')
def trainer_main(request):
    objects=Trainer_form.objects.all()
    context={'objects':objects}
    return render(request,'training/trainer_main.html',context=context)     

@login_required(login_url='login')
def trainer_form(request):
    form = TrainingForm()
    if request.method== "POST":
        form=TrainingForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('trainer_main')
    
    context = {'form':form}
    return render(request,'training/training_form.html',context)    

   

# blogs  
@login_required(login_url='login') 
def blogs(request):
    context = {'blogs': BlogModel.objects.all()}
    return render(request, 'blogs/blogs.html',context)

@login_required(login_url='login')
def blog_detail(request, id):
    context = {}
    try:
        blog_obj = BlogModel.objects.filter(id=id).first()
        blog_obj.view = blog_obj.view+1
        blog_obj.save()
        context['blog_obj'] = blog_obj
    except Exception as e:
        print(e)    
    return render(request, 'blogs/blog_detail.html',context)

@login_required(login_url='login')
def admin_see(request):
    context = {'blogs': BlogModel.objects.all()}
    return render(request , 'blogs/admin_see.html' ,context)

@login_required(login_url='login')
def admin_user_delete(request):
    context = {'userd' : User.objects.all()}    
    return render(request , 'blogs/user_delete.html' ,context)    
      

@login_required(login_url='login')
def see_blog(request):
    context = {}
    
    try:
        blog_objs = BlogModel.objects.filter(user = request.user)
        context['blog_objs'] =  blog_objs
    except Exception as e: 
        print(e)
    
    print(context)
    return render(request , 'blogs/see_blog.html' ,context)   


@login_required(login_url='login')    
def add_blog(request):
    context = {'form': BlogForm}

    try:
        if request.method == 'POST':
            form = BlogForm(request.POST)
            image = request.FILES['image']
            title = request.POST.get('title')
            link = request.POST.get('link')
            user = request.user

            if form.is_valid():
                content = form.cleaned_data['content']


            BlogModel.objects.create(
                title = title, content = content , link = link, image = image, user = user
            )
            return redirect('/blogs')

    except Exception as e:
        print(e)
    return render(request, 'blogs/add_blog.html',context)



@login_required(login_url='login')
def blog_delete_admin(request , id):
    try:
        blog_obj = BlogModel.objects.get(id = id)
        blog_obj.delete()
        messages.success(request, " Blog Delete Successfully")
        
    except Exception as e :
        print(e)

    return redirect('/view-admin')   
    
@login_required(login_url='login')
def remove_users(request, id):
    try:
        #users = BlogModel.objects.filter(id=id)
                
        User.objects.get(id=id).delete()
        
        #user.delete()
        #users.delete()
        
        messages.success(request, f"Successfully delete account ")

    except Exception as e:
        print(e)
        
    return redirect('/delete-users')
        

@login_required(login_url='login')
def blog_update(request,id):
    context = {}
    try:
        
        blog_obj = BlogModel.objects.get(id=id)
                
        if blog_obj.user != request.user:
            return redirect('/blogs')

        intial_dict = {'content': blog_obj.content}
        form = BlogForm(initial= intial_dict) 
        if request.method == 'POST':
            form = BlogForm(request.POST)
            image = request.FILES['image']
            title = request.POST.get('title')
            user = request.user

            if form.is_valid():
                content = form.cleaned_data['content']


            BlogModel.objects.create(
                title = title, content = content , image = image, user = user
            )   

        context['blog_obj'] = blog_obj  
        context['form'] = form  
        messages.success(request, " Blog Updated Successfully")


    except Exception as e:
        print(e)
    return render(request, 'blogs/update_blog.html', context)        
