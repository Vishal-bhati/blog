from django.views import generic
from django.shortcuts import render, redirect
from .forms import ContactForm, DjangoForm
from .models import Django, VisitCounter, Networking, Development

class AllPostsView(generic.TemplateView):
    def get(self, request):
        django_posts = Django.objects.filter(status=1) 
        development_posts = Development.objects.filter(status=1)
        networking_posts = Networking.objects.filter(status=1)
        
        context = self.get_context_data()
        context.update({
            'django_posts': django_posts,
            'development_posts': development_posts,
            'networking_posts': networking_posts
        })
        return render(request, 'index.html', context)

    def get_context_data(self, **kwargs):
        context = {}
        visit_counter, created = VisitCounter.objects.get_or_create()
        if created:
            visit_counter.save()
        visit_counter.count += 1 
        visit_counter.save()
        context['visit_counter'] = visit_counter
        return context


class DjangoList(generic.ListView):
    queryset = Django.objects.filter(status=1).order_by('-created_on')
    template_name = 'django.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        visit_counter, created = VisitCounter.objects.get_or_create()
        if created:
            visit_counter.save()
        visit_counter.count += 1 
        visit_counter.save()
        context['visit_counter'] = visit_counter
        return context

class DjangoDetail(generic.DetailView):
    model = Django
    template_name = 'django_detail.html'

class NetworkingList(generic.ListView):
    queryset = Networking.objects.filter(status=1).order_by('-created_on')
    template_name = 'networking.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        visit_counter, created = VisitCounter.objects.get_or_create()
        if created:
            visit_counter.save()
        visit_counter.count += 1 
        visit_counter.save()
        context['visit_counter'] = visit_counter
        return context

class NetworkingDetail(generic.DetailView):
    model = Networking
    template_name = 'networking_detail.html'
    
class DevelopmentList(generic.ListView):
    queryset = Development.objects.filter(status=1).order_by('-created_on')
    template_name = 'development.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        visit_counter, created = VisitCounter.objects.get_or_create()
        if created:
            visit_counter.save()
        visit_counter.count += 1 
        visit_counter.save()
        context['visit_counter'] = visit_counter
        return context

class DevelopmentDetail(generic.DetailView):
    model = Development
    template_name = 'development_detail.html'
    

class About(generic.TemplateView):
    template_name = 'about.html'



class Privacy(generic.TemplateView):
    template_name = 'privacy.html'

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_success')  # Redirect to a success page
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

def contact_success_view(request):
    return render(request, 'contact_success.html')

def create_post(request):
    if request.method == 'POST':
        form = DjangoForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            # Depending on the category selected, create the post for the corresponding model
            if category == 'Django':
                Django.objects.create(
                    title=form.cleaned_data['title'],
                    slug=form.cleaned_data['slug'],
                    author=form.cleaned_data['author'],
                    content=form.cleaned_data['content'],
                    status=form.cleaned_data['status'],
                    image=form.cleaned_data['image']
                )
            elif category == 'Networking':
                Networking.objects.create(
                    title=form.cleaned_data['title'],
                    slug=form.cleaned_data['slug'],
                    author=form.cleaned_data['author'],
                    content=form.cleaned_data['content'],
                    status=form.cleaned_data['status'],
                    image=form.cleaned_data['image']
                )
            elif category == 'Development':
                Development.objects.create(
                    title=form.cleaned_data['title'],
                    slug=form.cleaned_data['slug'],
                    author=form.cleaned_data['author'],
                    content=form.cleaned_data['content'],
                    status=form.cleaned_data['status'],
                    image=form.cleaned_data['image']
                )
            return redirect('home')
    else:
        form = DjangoForm()
    return render(request, 'create_post.html', {'form': form})