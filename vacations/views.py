from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import DreamVacation, Comment
from .forms import VacationForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Count

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
                                              

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'vacations/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
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

@login_required
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
