from django.urls import path
from . import views

app_name = 'Blog_App'

urlpatterns = [
 path('', views.BlogList.as_view(), name='blog_list'),
 path('write-new-blog/', views.CreateBlog.as_view(), name='write_new_blog'),
 path('blog/<slug:slug>/', views.BlogDetails.as_view(), name='blog_detail'),
 path('like/<pk>/', views.like, name='like'),
 path('unlike/<pk>/', views.unlike, name='unlike'),
 path('edit-blog/<slug:slug>/', views.BlogUpdate.as_view(), name='blog_update'),
 path('delete-blog/<slug:slug>/', views.BlogDelete.as_view(), name='blog_delete'),
 path('search-results/', views.SearchBlogs.as_view(), name='blog_search'),
]
