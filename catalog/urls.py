from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views as catalog_views


urlpatterns = [
    path('', views.index, name='index'),
    path('blogposts/', views.BlogpostListView.as_view(), name='blogposts'),
    path('blogpost/<int:pk>', views.BlogpostDetailView.as_view(), name='blogpost-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('authors/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('blog/<int:pk>/comment/', views.CommentCreate.as_view(), name='blogpost_comment'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
    path('blogpost/create/', views.BlogpostCreate.as_view(), name='blogpost-create'),
    path('blogpost/<int:pk>/update/', views.BlogpostUpdate.as_view(), name='blogpost-update'),
    path('blogpost/<int:pk>/delete/', views.BlogpostDelete.as_view(), name='blogpost-delete'),
    url(r'^signup/$', catalog_views.signup, name='signup'),
]

