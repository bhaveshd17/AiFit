from . import views
from django.urls import path

urlpatterns = [
    path('', views.home__page, name='home__page'),
    
    
    # path('home/',views.home, name='home'),
    path('video_feed/',views.video_feed, name='video_feed'),
    path('video_feed_rep/',views.video_feed_rep, name='video_feed_rep'),
    path('rtd_video_feed/',views.rtd_video_feed, name='rtd_video_feed'),
    # path('webcam_feed/',views.webcam_feed, name='webcam_feed'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
    path('check_form/', views.check_form, name='check_form'),
    path('check_form/<str:category>/', views.check_form_detection, name='check_form_detection'),
    path('upload_video_detection/<str:category>/', views.upload_video_detection, name='upload_video_detection'),
    
    path('rep_counter_biceps/', views.rep_counter_biceps, name='rep_counter_biceps'),
    
    path('analysis/', views.analysis__lookup, name='analysis'),
    
    path('signup/', views.sign_up__lookup, name='signup'),
    path('login/', views.login__lookup, name='login'),
    path('logout/', views.logout__lookup, name='logout'),


    #training
    path('training/<int:pk>', views.train, name='train'),
    path('trainer/', views.trainer_main, name='trainer_main'),
    path('trainer_form/', views.trainer_form, name='trainer_form'),

    #blogs
    path('blogs/',views.blogs, name='blogs'),
    path('add-blog/', views.add_blog, name = 'add_blog'),
    path('blog-detail/<str:id>', views.blog_detail , name='blog_detail'),
    path('view-blog/', views.see_blog , name='see_blog'),
    path('blog-delete/<str:id>',views.blog_delete_admin,name='blog_delete'),
    path('blog-update/<str:id>', views.blog_update, name='blog_update'),
    path('view-admin/', views.admin_see , name="admin_see"),
    path('delete-user/<str:id>', views.remove_users , name="remove_users"),
    path('delete-users/', views.admin_user_delete, name="admin_user_delete"),
]