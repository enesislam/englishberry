from django.contrib import admin

from .models import Post, Yazilar, AboutPosts,Category,GelenSorular, UserBio,UserImg,Hakkimizda,Comment


admin.site.register(Post)
admin.site.register(Yazilar)
admin.site.register(Comment)
admin.site.register(AboutPosts)
admin.site.register(Category)
admin.site.register(GelenSorular)
admin.site.register(UserBio)
admin.site.register(UserImg)
admin.site.register(Hakkimizda)
