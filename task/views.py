from django.shortcuts import render,redirect
from django.views.generic import View
from task.forms import RegistrationForm,LoginForm,TasksForm,TasksEditForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from task.models import Tasks
from django.utils.decorators import method_decorator


# Create your views here.

def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,'you have to login to perform this action')
            return redirect("signin")
        return fn(request,*args,**kwargs)        
    return wrapper
    
class SignUpView(View):
    model=User
    form_class=RegistrationForm
    template_name="register.html"

    def get(self,request,*args,**kwargs):
        form=self.form_class
        return render(request,self.template_name,{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
           form.save()
           messages.success(request,"account has been created ")
           return redirect("signin")  
        messages.error(request,"failed to create account")
        return render(request,self.template_name,{"form":form})
    
class SignInView(View):
    model = User
    form_class=LoginForm
    template_name="login.html"

    def get(self,request,*args,**kwargs):
        form=self.form_class
        return render(request,self.template_name,{"form":form})

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(username=uname,password=pwd)
            print(usr)
            if usr:

                login(request,usr)
                messages.success(request,"login success")
                return redirect("index")
        messages.error(request,"invalid credentials")
        return render(request,self.template_name,{"form":form})

# template inheritance
@method_decorator(signin_required,name='dispatch')   
class IndexView(View):
    template_name="index.html"

    def get(self,request,*args,**kwargs):
        return render(request,self.template_name)
        
            
# localhost:8000/tasks/add/

@method_decorator(signin_required,name='dispatch')
class TaskCreateView(View):
    model:Tasks
    form_class=TasksForm
    template_name="task-add.html"

    def get(self,request,*args,**kwargs):
        form=self.form_class
        return render(request,self.template_name,{"form":form})

    def post(self,request,*args,**kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            # instance=Tasks_object(task_name="template planning")
            form.instance.user=request.user
            form.save()
            # another method
            # task_obj=form.save(commit=True) #instance return on save
            # task_obj.user=request.user
            # task_obj.save()
            messages.success(request,"task has been added")
            return redirect("task-list")
        messages.error(request,"failed to add task")
        return render(request,self.template_name,{"form":form})
    
@method_decorator(signin_required,name='dispatch')
class TaskListView(View):
    model=Tasks
    template_name="task-list.html"

    def get(self,request,*args,**kwargs):       
        qs = self.model.objects.filter(user=request.user)
        return render(request,self.template_name,{"tasks":qs})

# localhost:8000/tasks/{id}/
@method_decorator(signin_required,name='dispatch')
class TaskDetailView(View):
    model=Tasks
    template_class="task-detail.html"
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=self.model.objects.get(id=id)
        return render(request,self.template_class,{"task":qs})

# localhost:8000/tasks/<init:pk>/change

@method_decorator(signin_required,name='dispatch')
class TaskEditView(View):
    model=Tasks
    form_class=TasksEditForm
    template_name="task-edit.html"

    def get(self,request,*args,**kwargs):
        id= kwargs.get("pk")
        obj=Tasks.objects.get(id=id)
        form=self.form_class(instance=obj)  # in normal form instead if instance initial is used and provide eavh filed value as dictionary
        return render(request,self.template_name,{"form":form})
    
    def post(self,request,*args,**kwargs):
         id= kwargs.get("pk")
         obj=Tasks.objects.get(id=id)
         form=self.form_class(instance=obj,data=request.POST)
         if form.is_valid():
             form.save()
             messages.success(request,"successfully updated")
             return redirect("task-list")
         messages.error(request,"failed to update task")   
         return render(request,self.template_name,{"form":form})     

#localhost:8000/tasks/<int:pk>/remove
@signin_required
def tasksDeleteView(request,*args,**kwargs):
    model=Tasks
    id=kwargs.get("pk")
    obj=Tasks.object.get(id=id)
    if obj.user == request.user:
        Tasks.objects.get(id=id).delete()
        messages.success(request,"deleted succesfully")
        return redirect("task-list")
    else:
        messages.error(request,"you don't have the permission to do this action")
        return redirect('signin')

def signoutView(request,*args,**kwargs):
    logout(request)
    messages.success(request,"You are logged out. Please login again")
    return redirect("signin")

