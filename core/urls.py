from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('hakkimizda/', views.about,name='about' ),
    path('yazilar/', views.yazilar, name='yazilar'),
    path('yazilar/<int:pk>', views.yazi_detail, name='yazi_detail'),
    path('iletisim/', views.contact, name='contact'),
    path("dersler/<slug:slug>", views.post_detail, name = "post-detail"),
    path("dersler", views.posts, name = "posts"),
    path("kategori/<str:cats>/", views.category, name = "category"),
    path('begen/', views.add_to_like, name='like'),
    path('delete_comment/', views.delete_comment, name='delete_comment'),
    path('sorusor/', views.AskToAdmin, name='sorusor'),
    path("hesabim/", views.profile, name="account_profile"),
    path("begendiklerim/", views.begendiklerim, name="begendiklerim"),
    path("mesajlarim/", views.mesajlarim, name="mesajlarim"),
    path("izlediklerim/", views.izlediklerim, name="izlediklerim"),
]
