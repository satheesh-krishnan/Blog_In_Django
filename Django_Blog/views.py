from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib import messages
from django.contrib.sessions.models import Session
from models import user,posts,comments
from forms import bform,loginn,signupp
import re
import os
import datetime
def login(request):
    f=loginn(request.POST)
    fb=bform(request.POST)
    if request.method=='POST':
        if request.POST.get('login'):
            if f.is_valid():
                l=[]
                cd=f.cleaned_data
                request.session['logi']=cd['logi']
                emails=user.objects.all()
                for each in emails:l.append(each.email)
                if cd['logi'] in l:
                    password=user.objects.filter(email=cd['logi'])
                    for each in password:l.append(each.password)
                    if cd['passw'] in l:return HttpResponseRedirect('/userr')
                    else:messages.error(request,'Wrong Password')
                else:messages.error(request,'Invalid Email')
        if request.POST.get('signup'):return HttpResponseRedirect('/signup')
        if request.POST.get('search'):
            if fb.is_valid():
                ce=fb.cleaned_data['sear']
                request.session['ce']=ce
                request.session['tmp']=False
                return HttpResponseRedirect('/search')
    return render(request,'login.html',{'f':f,'fb':fb})
def signup(request):
    f=signupp(request.POST)
    if request.method=='POST':
        if request.POST.get('signup'):
            if f.is_valid():
            	cd=f.cleaned_data
            	p=user(name=cd['name'],email=cd['l'],password=cd['p'])
            	p.save()
            	messages.success(request,'Saved')
        if request.POST.get('home'):return HttpResponseRedirect('/login')
    return render(request,'signup.html',{'f':f})
def search(request):
    l=[]
    z=[]
    ce=request.session['ce']
    tmp=request.session['tmp']
    pos=posts.objects.all()
    if ce!='':
        for each in pos:
            match=re.search(ce,each.post,re.IGNORECASE)
            if match:
                if each.status=='publish':
                    l.append(each)
    if len(l)==0:
        messages.error(request,'No Match Found')
    else:
        for each in l:
            r=open('blog'+'/'+'blogs'+'/'+each.pl)
            r=r.readlines()
            z.append((each,r[0]))
    return render(request,'search.html',{'z':z,'tmp':tmp})
def userr(request):
    f=bform(request.POST)
    logi=request.session['logi']
    nam=user.objects.filter(email=logi)
    nam=nam[0].name
    upost=posts.objects.filter(name=nam)
    request.session['nam']=nam
    tmp=True
    request.session['tmp']=tmp
    if request.method=='POST':
        if request.POST.get('create'):
            return HttpResponseRedirect('/create')
        if request.POST.get('search'):
            if f.is_valid():
                ce=f.cleaned_data
                request.session['ce']=ce['sear']
                request.session['tmp']=True
                return HttpResponseRedirect('/search')
        if request.POST.get('logout'):return HttpResponseRedirect('/login')
    return render(request,'posts.html',{'f':f,'upost':upost,'nam':nam})    
def create(request,context=-1):
    l=[]
    k=''
    new={}
    nam=request.session['nam']
    f=bform(request.POST)   
    if context != -1:
        b=posts.objects.filter(id=context)
        i=b[0].pl
        a=open('blog'+'/'+'blogs'+'/'+i)
        a=a.readlines()
        for each in a:
            k=k+each
        data={'head':str(b[0].post),'body':k}
        f=bform(initial=data)
    if request.method=='POST':
        if request.POST.get('publish'):
            dat=savee(request,nam,'publish')
            f=bform(initial=dat)
        if request.POST.get('save'):
            dat=savee(request,nam,'save')
            f=bform(initial=dat)
        if request.POST.get('refresh'):f=bform(initial='')
        if request.POST.get('home'):return HttpResponseRedirect('/userr')
        if request.POST.get('logout'):return HttpResponseRedirect('/login')
    return render(request,'create.html',{'f':f})
def reply(request,context):
    z=[]
    f=bform(request.POST)
    b=posts.objects.get(id=context)
    a=open('blog'+'/'+'blogs'+'/'+b.pl)
    k=a.readlines()
    e=comments.objects.filter(post=b.comment)
    for each in e:
        o=open('blog'+'/'+'command'+'/'+each.com)
        z.append((each,o.readlines()))
    if request.method=='POST':
        if request.POST.get('submit'):
            if f.is_valid():
                cd=f.cleaned_data
                time=datetime.datetime.now().time()
                fle=open('blog'+'/'+'command'+'/'+str(time),'a')
                fle.write('Reply \n \n')
                fle.write(cd['rly'])
                now=datetime.date.today()
                p=comments(post=b.comment,com=str(time),date=str(now.day)+'/'+str(now.month)+'/'+str(now.year))
                p.save()
                return HttpResponseRedirect('/'+context+'/reply')               
        if request.POST.get('home'):return HttpResponseRedirect('/userr')
        if request.POST.get('logout'):return HttpResponseRedirect('/login')
    return render(request,'reply.html',{'f':f,'k':k,'b':b,'z':z,'context':str(context)})
def blog(request,context):
    z=[]
    f=bform(request.POST)
    tmp=request.session['tmp']
    b=posts.objects.get(id=context)
    a=open('blog'+'/'+'blogs'+'/'+b.pl)
    k=a.readlines()
    e=comments.objects.filter(post=b.comment)
    for each in e:
        o=open('blog'+'/'+'command'+'/'+each.com)
        z.append((each.date,o.readlines()))
    if request.method=='POST':
        if request.POST.get('submit'):
            if f.is_valid():
                cd=f.cleaned_data
                time=datetime.datetime.now().time()
                fle=open('blog'+'/'+'command'+'/'+str(time),'a')
                fle.write(cd['com'])
                now=datetime.date.today()
                p=comments(post=b.comment,com=str(time),date=str(now.day)+'/'+str(now.month)+'/'+str(now.year))
                p.save()
                return HttpResponseRedirect('/'+context+'/blog')
        if request.POST.get('home'):
            if tmp:return HttpResponseRedirect('/userr')
            else:return HttpResponseRedirect('/login')
        if request.POST.get('logout'):return HttpResponseRedirect('/login')
    return render(request,'blog.html',{'f':f,'k':k,'tmp':tmp,'b':b,'z':z})
def savee(request,nam,status):
    f=bform(request.POST)
    a=''
    l=[]
    pos=posts.objects.filter(name=nam)
    now=datetime.datetime.now()
    time=datetime.datetime.now().time()
    if f.is_valid():
        cd=f.cleaned_data
        l=cd['head']
    for each in pos:
        if l==each.post:
            a=l
            break
    if len(a)>0:
        p=posts.objects.get(post=l)
        os.remove('blog'+'/'+'blogs'+'/'+p.pl)
        p.pl=str(time)
        p.date=str(now.day)+'/'+str(now.month)+'/'+str(now.year)
        p.status=status
        p.save()
    else:
        p=posts(name=nam,post=cd['head'],pl=str(time),comment=cd['head'][:5],cn=0,date=str(now.day)+'/'+str(now.month)+'/'+str(now.year),status=status)
        p.save()
    d=open('blog'+'/'+'blogs'+'/'+str(time),'w')
    d.write(cd['body'])
    d.close()
    d=open('blog'+'/'+'blogs'+'/'+str(time),'r')
    k=''
    q=d.readlines()
    for each in q:
        k+=each
    data={'body':k}
    return data 
def dele(request,context,context1):
    p=comments.objects.get(id=context)
    os.remove('blog'+'/'+'command'+'/'+p.com)
    p.delete()
    return HttpResponseRedirect('/'+context1+'/reply')    
