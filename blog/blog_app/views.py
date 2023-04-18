from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, DetailView
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from .forms import ContactForm, SearchForm, CommentForm
from .models import Post, Category, Comment

# Create your views here.


class CommonEntitiesMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['searchform'] = SearchForm()
        return context
    

class HomeView(CommonEntitiesMixin, TemplateView):
    template_name = 'index.html'
    article = "home"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # pk = self.kwargs.get('pk2')
        # category = Category.objects.filter(id=pk).first()
        context["posts"] = Post.objects.all().order_by('title')
        context["mostread"] = Post.objects.all().order_by('num_views')
        context['mostrecent'] = Post.objects.all().order_by('-publish_date')
        context["comments"] = Comment.objects.all()
        context["article"] = self.article
        return context


class PostDetailView(CommonEntitiesMixin, DetailView):
    model = Post
    template_name = "post_detail.html"

    def get_object(self):
        obj = super().get_object()
        obj.num_views += 1
        obj.save()
        return obj
     

class ContactView(FormView):
    template_name = 'contact_us.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['searchform'] = SearchForm()
        return context

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


def search_view(request):
    form = SearchForm()
    query = request.GET.get('search')
    if query:
        results = Post.objects.filter(title__icontains=query)
        return render(request, 'search.html', {'results': results, 'searchform': form, 'query': query, })
    return render(request, 'search.html', {'searchform': form})


def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'comment_form.html', {'form': form, 'post': post})


def add_reply(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            author = form.cleaned_data['author']
            text = form.cleaned_data['text']
            parent = Comment.objects.get(pk=comment.id)
            Comment.objects.create(
                post=post, author=author, text=text, parent=parent)
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'reply_form.html', {'form': form, 'post': post, 'comment': comment})
