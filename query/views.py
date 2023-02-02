from django.core import paginator
from django.http.request import host_validation_re
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from . import models
import pymysql
import datetime
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib.auth.decorators import login_required,permission_required

# coding=utf-8

def hello_index(request):
     return HttpResponse('Hello!你成功创建了一个试图')
     
def query_patient_by_id(request,pid):
     database_name = 'DigestiveD'
     #连接服务器
     db = pymysql.connect(host="localhost", user="root", password="syx62007", database="DigestiveD")
     #创建游标
     cursor = db.cursor()
     #查询数据
     query_elements = ['Age','CheckDate','Gender','PatientID']
     query_statement = "select Age,CheckDate,Gender,PatientId from patientbasicinfos where id='%s'"%(pid)
     cursor.execute(query_statement)
     data = cursor.fetchall()
     #后台打印
     print(data)
     #生成字典并返回为json到前端
     data = data[0]
     out_json = {}
     for j,name in enumerate(query_elements):
          out_json[name]=data[j]
     #断开连接
     db.close()
     return JsonResponse(out_json)


def sl1(request):
     #设置时间范围
     date_from = datetime.datetime(2015, 1, 1, 0, 0)
     date_to = datetime.datetime(2015, 3, 1, 0, 0)  
     #筛选  
     listp = models.Patientbasicinfos.objects.filter(checkdate__range=(date_from, date_to),gender="男",age__gt=50)
     return render(request, 'filter/sl1.html',locals())

def sl2(request):  
     #筛选
     listp = models.DLabeledimage.objects.filter(userid="Lin.Ne",pathtype="RECTANGLE",)
     dicto ={}
     #统计每个病人id出现的数量，即每个病人对应照片数量
     for i in listp:
          if i.patientid not in dicto.keys():
               dicto.update({i.patientid:1})
          else:
               dicto[i.patientid] =dicto[i.patientid]+1 
     #将结果以列表嵌套列表的形式呈现
     results=[]
     for k in dicto.keys():
          results.append([k,dicto[k]])
     return render(request, 'filter/sl2.html',locals())

def sl3(request):  
     #筛选
     listp = models.ALabeledimage.objects.filter(userid="Chen.Fei",pathtype="HAND",)
     listpath = []
     for k in listp:
          i = k.imageid
          try:
               #寻找对应path
               pathi=models.Imagepath.objects.get(imageid=i)
               listpath.append([k.patientid,i,pathi.imgpath])
          except:
               listpath.append('None')
     return render(request, 'filter/sl3.html',locals())

def sl4(request): 
     #筛选“糜烂”条目 
     listp = models.DArearoi.objects.filter(diseaseid="00600")
     #整理出“糜烂条目”对应的所有病人id
     Patients=[]
     for k in listp:
          i = k.areaid
          try:
               pi=models.DLabeledimage.objects.get(areaid=i)
               Patients.append(pi.patientid)
          except:
               Patients.append('None')
     #删除多次出现的病人条目
     np=[]
     for old in Patients:
          if old not in np:
               np.append(old)
     #根据病人id找到对应的病人信息，进一步筛选
     pf2=[]
     for i in np:
          try:
               pi2=models.Patientbasicinfos.objects.get(patientid=i)
               if (pi2.gender == "男") and (pi2.hospitalid == "001"):
                    #检验examinationfindings中是否有“糜烂”
                    if "糜烂" in pi2.examinationfindings:
                         pf2.append([pi2.patientid,pi2.gender,pi2.hospitalid,pi2.examinationfindings,'yes'])
                    else:
                         pf2.append([pi2.patientid,pi2.gender,pi2.hospitalid,pi2.examinationfindings,'no'])
          except:
               continue
     return render(request, 'filter/sl4.html',locals())




@login_required
def user_list(request):
    # 查询数据库用户数据
     if request.method == 'POST':
          #加入筛选限制条件
          pid=request.POST.get('patientid')
          age1=request.POST.get('patientage1')
          age2=request.POST.get('patientage2')
          sex=request.POST.get('patientsex')
          yin=request.POST.get('year_in')
          min=request.POST.get('month_in')
          din=request.POST.get('date_in')
          yout=request.POST.get('year_out')
          mout=request.POST.get('month_out')
          dout=request.POST.get('date_out')
          kwarg={}
          if pid.strip() != '':
               kwarg['patientid']=pid
          if age1.strip() != '':
               kwarg['age__range']=(int(age1),int(age2))
          #可增改
          if yin.strip() != '':
               date_from = datetime.datetime(int(yin), int(min), int(din), 0, 0)
               date_to = datetime.datetime(int(yout), int(mout), int(dout), 0, 0)
               kwarg['checkdate__range']=(date_from, date_to)
          if sex.strip() != '':
               kwarg['gender']=sex 
          user_ret = models.Patientbasicinfos.objects.filter(**kwarg)
     else:
          user_ret = models.Patientbasicinfos.objects.all()
     #翻页功能
     current_page = request.GET.get('page')
     paginator = Paginator(user_ret,10)
     try:
         posts=paginator.page(number = current_page)
     except PageNotAnInteger as e: #当前页面数非整数      
          posts = paginator.page(1)    
     except EmptyPage as e: #当前页码数为空
          posts = paginator.page(1)    
    # 返回给前端页面  
     return render(request ,'modify/user_list.html',{'posts':posts,}) 


# 删除数据
@permission_required('patientbasicinfos.delete_patientbasicinfos')
def delete_user(request):
    # 取出需要删除的id
    delete_id = request.GET.get('pid')
    pdelete_id = request.GET.get('ppid')
    # 从数据库删除的
    models.ALabeledimage.objects.filter(patientid=pdelete_id).delete()
    models.Patientbasicinfos.objects.filter(id=delete_id).delete()
    return redirect('/userlist/')

# 修改数据
def update_user(request):
    update_id = request.GET.get('pid')
    imgid = request.GET.get('imgid')
    item = request.GET.get('item')
    if request.method == 'POST':
        new_age = request.POST.get('age')
        # 找到匹配的id
        update_obj = models.Patientbasicinfos.objects.filter(id=update_id).first()
        # 新数据
        if item == 'age':
             update_obj.age=new_age
        if item == 'patientid':
             update_obj.patientid=new_age
        if item == 'checkdate':
             update_obj.checkdate=new_age
        if item == 'gender':
             update_obj.gender=new_age
        if item == 'patientname':
             update_obj.patientname=new_age
        if item == 'hospitalid':
             update_obj.hospitalid=new_age
        update_obj.save()
        return redirect('/userlist/')
    ret = models.Patientbasicinfos.objects.get(id=update_id)
    return render(request, 'modify/update_user.html', {'ret': ret,'item':item})

#增加条目
def add_user(request):
    error_name = ''
    if request.method == 'POST':
    # 1、获取前端输入的数据
        id = request.POST.get('pid')
        pid = request.POST.get('pid')
        CheckDate = request.POST.get('checkdate')
        Gender = request.POST.get('gender')
        pname = request.POST.get('pname')
        Age = request.POST.get('age')
        HospitalID = request.POST.get('hospitalid')
        user_list = models.Patientbasicinfos.objects.filter(patientid=pid)
         # 2、判断数据库是否存在
        if user_list :
                error_name = '用户名已经存在了'
                return  render(request,'modify/add_user.html',{'error_name':error_name})
        # 3、存储到数据库中
        else:
            user = models.Patientbasicinfos.objects.create(patientid=pid,checkdate=CheckDate,patientname=pname,gender=Gender,age=Age,hospitalid=HospitalID)
            user.save()
            return redirect('/userlist/')
    return render(request, 'modify/add_user.html')

def redunt_user(request):
     database_name = 'DigestiveD'
     #连接服务器
     db = pymysql.connect(host="localhost", user="root", password="syx62007", database="DigestiveD")
     #创建游标
     cursor = db.cursor()
     query_elements = ['Age','CheckNumber','CheckDate','Gender','PatientID']
     #选出patientid重复次数大于等于2次的条目
     query_statement = "select PatientID,count(*) as count from patientbasicinfos group by PatientID having count>1;"
     cursor.execute(query_statement)
     data = cursor.fetchall()
     db.close()
     flag = 0
     #对每个重复条目，抓取其其他信息
     for i in data:
          if flag == 0:
               user_ret = models.Patientbasicinfos.objects.filter(patientid=i[0])
               flag = 1
          else :
               user_ret = user_ret |models.Patientbasicinfos.objects.filter(patientid=i[0])
               
     current_page = request.GET.get('page')
     paginator = Paginator(user_ret,10)
     try:
         posts=paginator.page(number = current_page)
     except PageNotAnInteger as e: #当前页面数非整数      
          posts = paginator.page(1)    
     except EmptyPage as e: #当前页码数为空
          posts = paginator.page(1)    
    # 返回给前端页面  
     return render(request ,'modify/user_list.html',{'posts':posts}) 


def count_disease(request):
     all = models.Diseasedict.objects.all()
     dict={}
     for i in all:
          if i.diseaseid not in dict.keys():
               t = models.DArearoi.objects.filter(diseaseid=i.diseasename)
               dict.update({i.diseaseid:len(t)})
     results=[]
     for k in dict.keys():
          results.append([k,dict[k]])
     title=['疾病名称','标注数']
     return render(request, 'filter/sl2.html',{'results':results,'title':title})

def count_Anatomy(request):
     all = models.Anatomydict.objects.all()
     dict={}
     for i in all:
          if i.anatomyname not in dict.keys():
               t = models.DArearoi.objects.filter(diseaseid=i.anatomyid)
               dict.update({i.anatomyname:len(t)})
     results=[]
     for k in dict.keys():
          results.append([k,dict[k]])
     title=['解剖结构名称','标注数']
     return render(request, 'filter/sl2.html',{'results':results,'title':title})
     
def pinfo(request):
     return render(request,'query/pinfo.html')

def user2(request):
    # 查询数据库用户数据
     if request.method == 'POST':
          #加入筛选限制条件
          pid=request.POST.get('patientid')
          img=request.POST.get('imgid')
          kwarg={}
          if pid.strip() != '':
               kwarg['patientid']=pid
          if img.strip() != '':
               kwarg['imageid']=img
          user_ret = models.ALabeledimage.objects.filter(**kwarg)
     else:
          user_ret = models.ALabeledimage.objects.all()
     #翻页功能
     current_page = request.GET.get('page')
     paginator = Paginator(user_ret,10)
     try:
         posts=paginator.page(number = current_page)
     except PageNotAnInteger as e: #当前页面数非整数      
          posts = paginator.page(1)    
     except EmptyPage as e: #当前页码数为空
          posts = paginator.page(1)    
    # 返回给前端页面  
     return render(request ,'modify/user2.html',{'posts':posts}) 
     