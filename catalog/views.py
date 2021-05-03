from django.shortcuts import render

# Create your views here.
from catalog.models import Blogpost, Comment, Category, Author
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def index(request):
    num_blogpost = Blogpost.objects.all().count()
    num_author = Author.objects.all().count()
    num_category = Category.objects.all().count()

    # number of visit
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_blogpost': num_blogpost,
        'num_author': num_author,
        'num_category': num_category, 
        'num_visits': num_visits,
    }
    
    return render(request, 'index.html', context=context)

class BlogpostListView(generic.ListView):
    model = Blogpost
    paginate_by = 3

class BlogpostDetailView(generic.DetailView):
    model = Blogpost

class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 3

class AuthorDetailView(generic.DetailView):
    model = Author

class CategoryListView(generic.ListView):
    model = Category

class CommentCreate(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['post_comment',]

    def get_context_data(self, **kwargs):
        """
        Add associated blog to form template so can display its title in HTML.
        """
        # Call the base implementation first to get a context
        context = super(CommentCreate, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['blogpost'] = get_object_or_404(Blogpost, pk = self.kwargs['pk'])
        return context
        
    def form_valid(self, form):
        """
        Add author and associated blog to form data before setting it as valid (so it is saved to model)
        """
        #Add logged-in user as author of comment
        form.instance.writer = self.request.user
        #Associate comment with blog based on passed id
        form.instance.blogpost=get_object_or_404(Blogpost, pk = self.kwargs['pk'])
        # Call super-class form validation behaviour
        return super(CommentCreate, self).form_valid(form)

    def get_success_url(self): 
        """
        After posting comment return to associated blog.
        """
        return reverse('blogpost-detail', kwargs={'pk': self.kwargs['pk'],})

class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'picture']
    permission_required = 'catalog.can_create_author'

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = '__all__' # Not recommended (potential security issue if more fields added)
    permission_required = 'catalog.can_create_author'

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_create_author'
        
class BlogpostCreate(PermissionRequiredMixin, CreateView):
    model = Blogpost
    fields = ['title', 'author', 'category', 'content']
    permission_required = 'catalog.can_create_author'

class BlogpostUpdate(PermissionRequiredMixin, UpdateView):
    model = Blogpost
    fields = ['title', 'author', 'category', 'content']
    permission_required = 'catalog.can_create_author'

class BlogpostDelete(PermissionRequiredMixin, DeleteView):
    model = Blogpost
    success_url = reverse_lazy('Blogposts')
    permission_required = 'catalog.can_create_author'

    
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
        
        



