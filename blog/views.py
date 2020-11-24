from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from .forms import AddComment
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
# Create your views here.

#def home(request):
#	context = {
#		'posts': Post.objects.all()
#	}
#	return render(request, 'blog/home.html', context)


class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'
	context_object_name = 'posts'
	ordering = ['-date']
	paginate_by = 7


class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html'
	context_object_name = 'posts'
	paginate_by = 7

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date')


class PostDetailView(DetailView):
	model = Post

	def get_context_data(self, *args, **kwargs):
		context = super(PostDetailView, self).get_context_data()
		stuff = get_object_or_404(Post, id=self.kwargs['pk'])
		total_likes = stuff.total_likes()
		context['total_likes'] = total_likes
		return context


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	fields = ['title','content','post_pic']
	success_url= '/'

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	fields = ['title','content', 'post_pic']
	

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False


def Contact(request):
	if request.method == "POST":
		name = request.POST['message-name']
		email = request.POST['message-email']
		subject = request.POST['message-subject']
		messages_m = request.POST['message_body']

		send_mail(
			subject, #subject
			messages_m + "\nName:" + name, #message
			email, #from email
			['sam_olayemi65@yahoo.com'], #to email
			)
		return render(request, 'blog/contact.html', {'name': name})
	else:		
		return render(request, 'blog/contact.html', {})


class AddComment(LoginRequiredMixin, CreateView):
	model = Comment
	form_class = AddComment
	template_name = 'blog/user_comments.html'
	#success_url = '/'
	
	def get_success_url(self):
		return reverse_lazy('detail', kwargs={'pk':self.kwargs['pk']})

	
	def form_valid(self, form):
		form.instance.post_id = self.kwargs['pk']
		form.instance.authors = self.request.user
		return super().form_valid(form)


		
	

@login_required
def LikeView(request, pk):
	#post = get_object_or_404(Post, id=request.POST.get('post_id'))
	post = Post.objects.get(id=pk)
	post.likes.add(request.user)
	return HttpResponseRedirect(reverse('detail', args=[str(pk)]))



	


	



	
	
