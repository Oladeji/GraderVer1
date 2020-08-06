from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import  UserCreationForm
from django.contrib.auth import  login, authenticate,logout
from .forms import UserLoginForm ,UserRegisterForm
import requests
import json
from pyexcelerate import Workbook
from django.http import HttpResponse
from pyexcelerate import Workbook, Color, Style, Font, Fill, Format
from datetime import datetime
# Create your views here.
# def index(request):
#     return render(request,'GradeManager/login.html',{})

#@login_required


def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None) 
    if form.is_valid():
       username = form.cleaned_data.get('username')
       password = form.cleaned_data.get('password')
       user = authenticate(username=username,password=password)
       if not user :
               raise forms.ValidationError('This user does not exist')
       if not user.check_password(password):
                  raise forms.ValidationError('In Correct password')
       if not user.is_active:
                  raise forms.ValidationError('This user is not active')
       login(request,user)
       if next :
            return redirect(next)
       #return redirect('testing')
       return redirect('landing')
    else:
        form = UserLoginForm()
    context ={'form' : form }
    return render(request,'registration/loginview.html',context)



def register_view(request):
        next = request.GET.get('next')
    #if request.method == 'POST':
        form = UserRegisterForm(request.POST or None) 
        if form.is_valid():
            user = form.save(commit=False)
            #form.save()
            username = form.cleaned_data['username']
            password=form.cleaned_data['password']
            user.set_password(password)
            user.save()
            new_user = authenticate(username=username,password=password)
            login(request,new_user)
            if next :
                return redirect(next)
            return redirect('landing')
    #else:
    #    form = UserRegisterForm() 
        context ={'form' : form }
        return render(request,'registration/registerview.html',context)


def logout_view(request):
    logout(request)
    return redirect('landing')


def landing(request):
    print(request.user)
    return render(request,'GradeManager/landing.html',{})



def testing(request):
    print(request.user)
    return render(request,'GradeManager/testing.html',{})


@login_required
def AvailableCourses_view(request):

    api='http://192.168.0.111/onlinecoursereg/api/Camp/getCourses'
    try:
          r = requests.get(api)
          courselist = json.loads(r.text)
          print('loaded')
          for i in  courselist: 
            print(i['MYCOURSEID'] ,' ==> ',i['MYCOURSENAME']) 
            print('_____________________________\n') 
    except  Exception as inst:
          print(inst)
    return render(request,'GradeManager/availableCourses.html',{'courselist':courselist})




def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'
    if request.session.has_key('courselist'):
         courselist = request.session['courselist']
         workbook = Workbook()
         worksheet = workbook.new_sheet('Sheet1')

         print(courselist)
         col_start=0
         row_start=7
         worksheet.set_cell_value(1 ,1,'SECRETKEY')
         worksheet.set_cell_value(3 ,2,'THE POLYTECHNIC IBADAN')
         worksheet.set_cell_value(4 ,2,'DEAPRTMENT')
         worksheet.set_cell_value(4 ,2,'COURSE CODE SESSION SEMESTER ')
         worksheet.set_cell_value(5 ,2,' CCOURSE CODE : '+courselist[0]['MYCOURSEID'])
         worksheet.range("B3", "E3").merge()
         worksheet.range("B4", "E4").merge()
         worksheet.range("B5", "E5").merge()
         
         worksheet.set_cell_style(1, 1, Style(font=Font(bold=True)))
         worksheet.set_cell_style(1, 1, Style(font=Font(italic=True)))
         worksheet.set_cell_style(1, 1, Style(font=Font(underline=True)))
         worksheet.set_cell_style(1, 1, Style(font=Font(strikethrough=True)))
         worksheet.set_cell_style(1, 1, Style(fill=Fill(background=Color(255,0,0,0))))
         worksheet.set_cell_value(1, 2, datetime.now())
         worksheet.set_cell_style(1, 1, Style(format=Format('mm/dd/yy')))
         for index,row in  enumerate(courselist): 
           
            #'MYSURNAME': 'IBIDUN', 'MYMIDDLENAME': 'ABIODUN', 'MYFIRSTNAME': 'OLUWATOBI', 'MYSTUDENTID': '2014070101249', 'MYASESSIONID': '2017/2018', 'MYSEMESTERID': '1', 'MYCOURSEID': 'ACC316', 'MYASETID': '2017', 'MYLEVELTODO': '400', 'MYCOURSEUNIT': 2.0, 'MYCOURSENATURE': 'E', 'MYCOURSESTATE': 'R', 'MYSCORE': 48, 'MYAUSERID': 1, 'MYDONEDATE': '2019-09-09T00:00:00', 'MYREADONLY': 'F', 'MYMODIFIED': True, 'MYNAME': 'IBIDUN  ABIODUN  OLUWATOBI'}
            #print(row['MYSURNAME'] ,' ==> ',row['MYSTUDENTID']) 
            #'MYASESSIONID': '2017/2018', 'MYSEMESTERID': '1', 'MYCOURSEID': 'ACC316', 'MYASETID': '2017', 'MYLEVELTODO': '400', 'MYCOURSEUNIT': 2.0, 'MYCOURSENATURE': 'E', 'MYCOURSESTATE': 'R', 'MYSCORE': 48, 'MYAUSERID': 1, 'MYDONEDATE': '2019-09-09T00:00:00'
             
             worksheet.set_cell_value(index+row_start ,col_start+1,index+1)
             worksheet.set_cell_value(index+row_start ,col_start+2,row['MYSTUDENTID'])
             worksheet.set_cell_value(index+row_start ,col_start+3,row['MYSURNAME'])
             worksheet.set_cell_value(index+row_start ,col_start+4,row['MYMIDDLENAME'])
             worksheet.set_cell_value(index+row_start ,col_start+5,row['MYFIRSTNAME'])
            
             worksheet.set_cell_value(index+row_start ,col_start+6,row['MYSCORE'])
            # worksheet.set_cell_value(index+5 ,6,row['MYMIDDLENAME'])
            #worksheet[row][1].value = row['MYSURNAME'] # a number
            #worksheet[row][2].value = row['MYSTUDENTID']
         workbook.save(response)
    else:
        print('Nothing was passed in session')

    #wb.save("output.xlsx")
    #wb.save(response)
    return response


@login_required
def displayCourse_view(request, csrid):  
    courselist={}
  #if request.method=='POST or None':
    ploads = {'csrid':csrid,'year':'1920'}
    #api='http://192.168.8.103/onlinecoursereg/api/Student/PythonPullForscoreEntry?data='+csrid
    api='http://192.168.0.111/onlinecoursereg/api/Student/Python'

    try:

          headers = {'content-type': 'application/json'}
          r = requests.post(api,json=ploads,headers=headers)
          courselist = json.loads(r.text)
          try:
             del request.session['courselist']
          except KeyError:
            pass
          request.session['courselist'] = courselist
          for i in  courselist: 
            print(i['MYSURNAME'] ,' ==> ',i['MYSTUDENTID']) 
            print('_____________________________\n') 
    except  Exception as inst:
          print(inst)
    return render (request,'GradeManager/mycourselist.html',{'courselist':courselist})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            return redirect('landing')
    else:
        form = UserCreationForm()

    context ={'form' : form }
    return render(request,'registration/register.html',context)