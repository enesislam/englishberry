from django.shortcuts import render
from .models import (
    Post,AboutPosts,
    Category, GelenSorular,
    UserBio,
    UserImg,
    Hakkimizda,
    Comment,
    Yazilar,

    )

from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.shortcuts import redirect
import json
from django.http import JsonResponse
from django.core.files.base import ContentFile
import base64
from django.core.files.storage import FileSystemStorage

def processorus_category(request):
	cates = Category.objects.all().values_list()
 
	return {cates}
# Create your views here.
def home(request):
    context={
        'posts':Post.objects.filter(published=True).order_by('-date_added')[:6],
        'yazilar':Yazilar.objects.filter(published=True).order_by('-date_added')[:6],

        }
    return render(request, 'home.html',context)


def post_detail(request, slug):
    q = get_object_or_404(Post, slug = slug)
    cmmnt = Comment.objects.filter(post=q)

    # Beğen
    already_liked=[]
    id=request.user.id
    if(q.likes.filter(id=id).exists()):
        already_liked.append(q.id)

    # Yorumlar
    if request.method == 'POST':
        if request.POST.get("operation") == "submit_comment":
            text = request.POST.get('text', None)
            post = get_object_or_404(Post, slug = slug)
            user = request.user
            comment = Comment.objects.create(
                post = post,
                user = user,
                text = text
                )
            if comment.text == '':
                comment.delete()

            ctx = {
            'user':comment.user.username,
            'text':comment.text,
            }

            return JsonResponse(ctx)

    # Yorum Sil
    if request.method == 'POST':
        if request.POST.get("operation") == "delete_comment":
            post = get_object_or_404(Post, slug = slug)
            comment_id = request.POST.get('cmnt_id', None)
            comment = get_object_or_404(Comment, id = comment_id)
            comment.delete()
            print(comment_id)
            return JsonResponse({'comment_id':comment_id})
      
    ctx = {
    'comments':cmmnt,
    'content':q,
    'already_liked':already_liked
    }
    return render(request, 'post.html', ctx)

def delete_comment(request):
    if request.method == "POST":
        if request.POST.get("operation") == 'delete_comment':
            comment_id=request.POST.get("comment_id",None)
            comment=get_object_or_404(Comment, id=comment_id)
            comment.delete()
            ctx = {
            'comment_id':comment_id,
            'msg':'Silindi'
            } 
        return JsonResponse(ctx)

def posts(request):
    if request.method =="POST":
        if request.POST.get("operation") == "like_submit":
            content_id=request.POST.get("content_id",None)
            content=get_object_or_404(Post,pk=content_id)
        if content.likes.filter(id=request.user.id): #already liked the content
            content.likes.remove(request.user) #remove user from likes 
            liked=False
        else:
            content.likes.add(request.user) 
            liked=True
        ctx={"likes_count":content.total_likes(),"liked":liked,"content_id":content_id}
        return JsonResponse(ctx)
    contents=Post.objects.all()
    already_liked=[]
    id=request.user.id
    for content in contents:
        if(content.likes.filter(id=id).exists()):
            already_liked.append(content.id)
        ctx={"contents":contents,"already_liked":already_liked, 'name':'Tüm Dersler'}
    return render(request,'posts.html',ctx)

def add_to_like(request):
    if request.method == 'POST':
        slug = request.POST.get('slug', None)
        item = get_object_or_404(Post, slug=slug)
        if item.likes.filter(id=request.user.id): #already liked the content
            item.likes.remove(request.user) #remove user from likes 
            liked=False
        else:
            item.likes.add(request.user)
            liked=True
    ctx = {'likes_count': item.total_likes(), "liked":liked}
    return JsonResponse(ctx)

def category(request, cats):
    if request.method =="POST":
        if request.POST.get("operation") == "like_submit":
            content_id=request.POST.get("content_id",None)
            content=get_object_or_404(Post,pk=content_id)
        if content.likes.filter(id=request.user.id): #already liked the conten
            content.likes.remove(request.user) #remove user from likes 
            liked=False
        else:
            content.likes.add(request.user) 
            liked=True
            ctx={"likes_count":content.total_likes(),"liked":liked,"content_id":content_id}
            return JsonResponse(ctx)
    choices = Category.objects.get(name=cats)
    contents = Post.objects.filter(category=choices).order_by('-date_added')
    already_liked=[]
    id=request.user.id
    for content in contents:
        if(content.likes.filter(id=id).exists()):
            already_liked.append(content.id)
        ctx={"contents":contents,"already_liked":already_liked, 'name':choices}
        return render(request,'categories.html',ctx)
"""if you try to use "filter" 
		instead of "get" you will got an error 
		due of you have only one category to 
		keep so you need to use "get"
"""
def about(request):
    posts_in_about = AboutPosts.objects.all().order_by('-date_added')[:3]
    hakkimizda = Hakkimizda.objects.all().order_by('-date_added')[:1]
    ctx = {'posts':posts_in_about,'hakkimizda':hakkimizda}
    return render(request, 'about.html',ctx)

def contact(request):
	return render(request, 'contact.html')


def profile(request):
    if request.user.is_authenticated:
        soru_counter = GelenSorular.objects.filter(user=request.user).count()
        if UserBio.objects.filter(user=request.user).exists():
            user_bio_statue = UserBio.objects.filter(user=request.user).order_by('-date_added')[:1]

        else:
            user_bio_statue = None

        # Soru Sil
        if request.POST.get("operation") == "delete_soru":
            content_id = request.POST.get('content_id', None)
            soru = get_object_or_404(GelenSorular,id=content_id )
            soru.delete()
            response = {'msg':'Silindi','content_id':content_id}
            if soru_counter == 1:
                response = {'msg':'Mesaj Yok','content_id':content_id, 'bos_gari':'bos_gari'}

            return JsonResponse(response)
        # Kullanıcı Bio ekleme
        if request.method =="POST":
            if request.POST.get("operation") == "add_bio":
                text = request.POST.get('text', None)
                UserBio.objects.create(
                    user=request.user,
                    text=text
                    )
                if UserBio.objects.filter(user=request.user).exists():
                    user_old_bio = UserBio.objects.filter(user=request.user).order_by('date_added')[:1]
                    oldlan = get_object_or_404(user_old_bio)
                response = {'msg':'Bio eklendi', 'bio':text}
                return JsonResponse(response)

        # Kullanıcı Profile resim ekleme
        user_pp_statue = UserImg.objects.filter(user=request.user).order_by('-date_added')[:1]
        if UserImg.objects.filter(user=request.user).exists():
            user_pp_statue = UserImg.objects.filter(user=request.user).order_by('-date_added')[:1]
        else:
            UserImg.objects.create(user=request.user)
            user_pp_statue = UserImg.objects.filter(user=request.user).order_by('-date_added')[:1]
        if request.method =="POST":
            if request.POST.get("operation") == "add_pp":
                image1 = request.FILES.get("image")
                print(image1.name,'*'*25)
                fs = FileSystemStorage()
                image = fs.save(image1.name,image1)
                UserImg.objects.create(
                    user=request.user,
                    image=image
                    )
                print(image)
                if UserImg.objects.filter(user=request.user).exists():
                    user_old_img = UserImg.objects.filter(user=request.user).order_by('date_added')[:1]
                    oldlan = get_object_or_404(user_old_img)
                    oldlan.delete()
                response = {'pp': image}
                return JsonResponse(response)

        likelarim = Post.objects.filter(likes=request.user)[:3]
        sorularim = GelenSorular.objects.filter(user=request.user).order_by('-date_added')
        ctx={'like':likelarim,'sorduklarim':sorularim, 'user_bio_statue':user_bio_statue, 'user_pp_statue':user_pp_statue}
        return render(request, 'user/account_profile.html',ctx)
    else:
        return render(request, 'account/login.html')

def mesajlarim(request):
	return render(request, 'user/contact.html')

def izlediklerim(request):
	return render(request, 'user/contact.html')

def yazilar(request):
    yazilar = Yazilar.objects.filter(published=True)
    ctx = {'contents':yazilar,'name':'Makaleler'}
    return render(request, 'yazilar.html',ctx)



def yazi_detail(request, pk):
    q = get_object_or_404(Yazilar,id = pk)
    return render(request, 'yazi_detail.html',{'yazi':q})


def begendiklerim(request):
    likelarim = Post.objects.filter(likes=request.user)
    ctx = {'contents':likelarim,'name':'Beğendiklerim'}
    return render(request, 'user/begendiklerim.html',ctx)

def AskToAdmin(request):
    if request.method == "POST":
        name = request.user.username # getting data from first_name input 
        email = request.POST.get('email', None)  # getting data from last_name input
        text = request.POST.get('text', None) # getting data from last_name input
        if request.POST.get('name', None):
            name = request.POST.get('name', None) # getting data from last_name input
        else:
            name = request.user.username

        if text and email:
            if request.user.is_authenticated:
                GelenSorular.objects.create(
                user=request.user,
                name=name,
                kullanıcı_kayıtlı_mı='Evet',
                email=email,
                text=text,)
            else:
                GelenSorular.objects.create(
                name=name,
                kullanıcı_kayıtlı_mı='Hayır',
                email=email,
                text=text,)
            response = {
            'msg':'Mesaj gönderildi ', # response message
            'name':name,
            'email':email,
            'text':text,
            'gech':'sorun_yok'
            }
        elif not text:
            response = {
            'msg':'Yazı alanı boş. Doldurun tekrar deneyin ', # response message
            'name':name,
            'email':email,
            'text':'Girilmedi',
            }
        elif not email:
            response = {
            'msg':'E-posta alanı boş. Doldurun tekrar deneyin ', # response message
            'name':name,
            'email':'Girilmedi',
            'text':text,
            }
        else:
            response = {
            'msg':'Alanları doldurun ', # response message
            'name':name,
            'email':email,
            'text':text,
            }

        return JsonResponse(response) # return response as JSON
