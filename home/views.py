from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, View, DeleteView
from django.views.generic.edit import FormMixin, CreateView, UpdateView
from django.core.mail import send_mail, EmailMessage
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics
from .serializers import PostSerializer
from .forms import EmailPostForm, UserForm
from .models import Post



class PostListView(ListView):
    queryset = Post.objects.filter(status='published')
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'home/post/list.html'


class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'home/post/detail.html'


class PostListSerializer(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailSerializer(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostCreate(CreateView):
    model = Post
    fields = ['author', 'title', 'slug', 'body', 'status']

class PostUpdate(UpdateView):
    model = Post
    fields = ['author', 'title', 'slug', 'body', 'status']

class PostDelete(DeleteView):
    model = Post
    context_object_name = 'post'

    def get(self, request, pk):
        form = self.model.objects.get(pk=pk)
        form.delete()

        return redirect('home:post_list')


def post_share(request, pk):
    post = get_object_or_404(Post, pk=pk, status='published')
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request
            subject = 'Read it {}'.format(cd['name'],cd['email'], post.title)
            message = 'Read it "{}" on side {}\n\n It was add by {}: {}'.format(post.title,
                                                                                post_url,
                                                                                cd['name'],
                                                                                cd['comments'])
            send_mail(subject, message, 'bartlomiej.kubik@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
        sent = False
    return render(request, 'home/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})


class PostShare(FormMixin, ListView, EmailMessage):
    queryset = Post.objects.all()
    form_class = EmailPostForm
    success_url = 'home/post/list.html'
    template_name = 'home/post/share.html'

    def post(self):
        pass


    def form_valid(self, form):
        form.send_mail()
        #return super(EmailPostForm, self).form_valid(form)
        return super(PostShare, self).form_valid(form)


class UserFormView(View):
    form_class = UserForm
    template_name = 'home/post/registration_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():
          user = form.save(commit=False)

          username = form.cleaned_data['username']
          password = form.cleaned_data['password']
          user.set_password(password)
          user.save()

          user = authenticate(username=username, password=password)

          if user is not None:

              if user.is_active:
                login(request, user)
                return redirect('home:post_list')

        return render(request, self.template_name, {'form': form})


class UserLogIn(View):
    form_class = UserForm
    template_name = 'home/post/log_in.html'
    success_url = 'home/post/list.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home:post_list')


        return render(request, self.template_name, {'form': form})


class UserLogout(View):
    form_class = UserForm
    #success_url = 'home/post.log_in.html'

    def get(self, request):
        logout(request)
        return redirect('home:log_in')














