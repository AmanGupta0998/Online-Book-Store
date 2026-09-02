from django.urls import path
from . import views 

urlpatterns = [
    
    path('admindash/',views.admindash,name='admindash'),
    path('adminlogout/',views.adminlogout,name='adminlogout'),
    path('viewenq/',views.viewenq,name='viewenq'),
    path('delenq/<id>',views.delenq,name='delenq'),
    path('adminchangepwd/',views.adminchangepwd,name='adminchangepwd'),
    path('addcat/',views.addcat,name='addcat'),
    path('viewcat/',views.viewcat,name='viewcat'),
    path('addbook/',views.addbook,name='addbook'),
    path('viewbook/',views.viewbook,name='viewbook'),
    path('delcat/<id>',views.delcat,name='delcat'),
    path('delbook/<id>',views.delbook,name='delbook'),
    path('adminorders/',views.adminorders,name='adminorders'),
    path('editbook/<id>', views.editbook, name='editbook'),
   
   
]   