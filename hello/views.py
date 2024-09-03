from django.shortcuts import render,HttpResponse,redirect

# Create your views here.

def admin_user(request):
   if request.user.is_authenticated:
      if not request.user.is_superuser:
         return redirect("/")
   return render(request,'admin/admin.html')
# def user_services(request):
#     return render(request,'services.html')