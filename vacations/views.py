from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import DreamVacation, Comment, Profile
from .forms import VacationForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Count
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
# def get_theme_preference(request):
#     # Logic to fetch theme preference (example: from session or DB)
#     # theme = request.session.get('theme')  # Default to 'light' theme
#     return JsonResponse({'theme': theme})

class CustomLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:  # Redirect if user is already logged in
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

@login_required
def get_user_theme(request):
    # Assuming the theme is stored in the user's profile model
    theme = request.user.profile.theme_preference  # Replace 'profile.theme' with your actual field
    return JsonResponse({'theme': theme})

@login_required
def toggle_theme(request):
    profile = request.user.profile
    new_theme = request.GET.get('theme', 'light')
    profile.theme_preference = new_theme
    profile.save()
    return JsonResponse({'status': 'success', 'theme': new_theme})

def dynamic_search(request):
    query = request.GET.get('q', '')
    results = DreamVacation.objects.filter(title__icontains=query)
    results_data = [{'id': result.id, 'title': result.title, 'description': result.description, 'image_url' : result.image.url} for result in results]
    
    return JsonResponse({'results': results_data})

@login_required
def favorites(request):
    # Get the current user's favorites
    favorite_vacations = request.user.profile.favorites.all()
    return render(request, 'vacations/favorites.html', {'vacations': favorite_vacations})

@login_required
def toggle_favorite(request, vacation_id):
    if request.method == "POST":
        try:
            vacation = DreamVacation.objects.get(id=vacation_id)
            profile = request.user.profile

            if vacation in profile.favorites.all():
                profile.favorites.remove(vacation)
                favorited = False
            else:
                profile.favorites.add(vacation)
                favorited = True

            return JsonResponse({"success": True, "favorited": favorited})
        except DreamVacation.DoesNotExist:
            return JsonResponse({"success": False, "error": "Vacation not found."})

    return JsonResponse({"success": False, "error": "Invalid request."})

def vacation_detail(request, id):
    vacation = get_object_or_404(DreamVacation, id=id)
    comments = vacation.comments.annotate(upvote_count=Count('upvotes')).order_by('-upvote_count') 
    

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.vacation = vacation
            comment.user = request.user
            comment.save()
            return redirect('vacation_detail', id=id)
    else:
        form = CommentForm()

    return render(request, 'vacations/vacation_detail.html', {'vacation': vacation, 'comments': comments, 'form': form})

   

@login_required
def upvote_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        user = request.user

        if user in comment.upvotes.all():
            comment.upvotes.remove(user)
            status = 'removed'
        else:
            comment.upvotes.add(user)
            status = 'added'

        return JsonResponse({
            'success': True,
            'comment_id': comment.id,
            'upvotes': comment.total_upvotes(),
            'status': status,
        })

    return JsonResponse({'success': False, 'message': 'Invalid request'})


@login_required
@csrf_exempt
def add_comment(request, vacation_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON request body
            text = data.get('text')
            if not text:
                return JsonResponse({'success': False, 'message': 'Comment text is required'}, status=400)

            vacation = get_object_or_404(DreamVacation, id=vacation_id)
            comment = Comment.objects.create(
                vacation=vacation,
                user=request.user,
                text=text,
            )

            return JsonResponse({
                'success': True,
                'comment': {
                    'id': comment.id,
                    'text': comment.text,
                    'username': request.user.username,
                    'upvotes': 0,  # Initialize upvotes to 0
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)
                                              

def check_logged_in(request):
    is_logged_in = request.user.is_authenticated  # True if user is logged in, otherwise False
    return JsonResponse({'isLoggedIn': is_logged_in})


def user_login(request):
    # Redirect logged-in users trying to access the login page
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = redirect('home')
            return response
    else:
        form = AuthenticationForm()

    return render(request, 'vacations/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')

def register(request):
    # Redirect logged-in users trying to access the login page
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)  
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'vacations/register.html', {'form': form})

def home(request):
    vacations = DreamVacation.objects.all()
    top_vacation = max(vacations, key=lambda v: v.interaction_score(), default=None)
    categories = ['Beach', 'Hiking', 'Cottage', 'Cruise', 'Others']
    category_vacations = {}
    for category in categories:
        category_vacations[category] = DreamVacation.objects.filter(
            category=category
        )[:4]

    context = {
        'top_vacation': top_vacation,
        'category_vacations': category_vacations,
    }
    return render(request, 'vacations/home.html', context)

def category_view(request, category):
    # Annotate each vacation with the interaction score
    vacations = DreamVacation.objects.filter(category=category).annotate(
        interaction_score=Count('comments') + Count('comments__upvotes')
    ).order_by('-interaction_score')

    return render(request, 'vacations/category.html', {'vacations': vacations, 'category': category})

@login_required(login_url='login')
def create_vacation(request):
    if request.method == 'POST':
        form = VacationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = VacationForm()
    return render(request, 'vacations/create.html', {'form': form})






def search(request):
    query = request.GET.get('q', '')
    results = DreamVacation.objects.filter(title__icontains=query)
    return render(request, 'vacations/search.html', {'query': query, 'results': results})
