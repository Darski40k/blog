from django.shortcuts import HttpResponseRedirect, Http404
from django.views.generic import CreateView, UpdateView, ListView, DetailView, DeleteView
from .models import Blog, Likes
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
from django.utils.text import slugify
from unidecode import unidecode
from django.views.generic.edit import FormMixin
from .forms import CommentForm


class BlogList(ListView):
    context_object_name = 'blogs'
    model = Blog
    template_name = 'Blog_App/blog_list.html'


class CreateBlog(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = 'Blog_App/create_blog.html'
    fields = ('title', 'content', 'image')

    def form_valid(self, form):
        blog_object = form.save(commit=False)
        blog_object.author = self.request.user
        title = blog_object.title
        blog_object.slug = slugify(unidecode(title)) + '-' + str(uuid.uuid4())
        blog_object.save()
        return HttpResponseRedirect(reverse('index'))


class BlogDetails(LoginRequiredMixin, FormMixin, DetailView):
    model = Blog
    template_name = 'Blog_App/blog_details.html'
    context_object_name = 'blog'
    form_class = CommentForm

    def get_success_url(self):
        return reverse_lazy('Blog_App:blog_detail', kwargs={'slug': self.object.slug})

    def like(self):
        blog = self.get_object()
        like_check = Likes.objects.filter(blog=blog, user=self.request.user)
        if like_check:
            liked = True
        else:
            liked = False
        return liked

    def get_context_data(self, **kwargs):

        context = super(BlogDetails, self).get_context_data(**kwargs)
        context['form'] = CommentForm(initial={'post': self.object})
        context['like_check'] = self.like()
        return context

    def post(self, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        blog = self.get_object()
        comment_form = form.save(commit=False)
        comment_form.blog = blog
        comment_form.author = self.request.user
        comment_form.save()
        return super(BlogDetails, self).form_valid(form)


@login_required
def like(request, pk):

    blog = Blog.objects.get(pk=pk)
    user = request.user
    like_check = Likes.objects.filter(blog=blog, user=user)
    if not like_check:
        like_blog = Likes(blog=blog, user=user)
        like_blog.save()
    return HttpResponseRedirect(reverse('Blog_App:blog_detail', kwargs={'slug': blog.slug}))


@login_required
def unlike(request, pk):

    blog = Blog.objects.get(pk=pk)
    user = request.user
    like_check = Likes.objects.filter(blog=blog, user=user)
    like_check.delete()
    return HttpResponseRedirect(reverse('Blog_App:blog_detail', kwargs={'slug': blog.slug}))


class BlogUpdate(LoginRequiredMixin, UpdateView):
    model = Blog
    fields = ['title', 'content', 'image']
    template_name = 'Blog_App/edit_blog.html'

    def dispatch(self, request, *args, **kwargs):
        blog = self.get_object()
        if request.method == 'GET':
            if blog.author != request.user:
                raise Http404
            else:
                return self.get(request, *args, **kwargs)

    def get_success_url(self, **kwargs):
        return reverse_lazy('Blog_App:blog_detail', kwargs={'slug': self.object.slug})


class BlogDelete(LoginRequiredMixin, DeleteView):
    model = Blog
    template_name = 'Blog_App/delete_blog.html'
    context_object_name = 'blog'

    def get_success_url(self, **kwargs):
        return reverse_lazy('Blog_App:blog_list')

    def dispatch(self, request, *args, **kwargs):
        blog = self.get_object()
        if request.method == 'GET':
            if blog.author != request.user:
                raise Http404
            else:
                return self.get(request, *args, **kwargs)


class SearchBlogs(LoginRequiredMixin, ListView):
    template_name = 'Blog_App/search_results.html'
    model = Blog
    context_object_name = 'blogs'

    def get_queryset(self, **kwargs):
        queryset = super(SearchBlogs, self).get_queryset(**kwargs)
        return queryset.filter(title__contains=self.request.GET.get('key_words'))
