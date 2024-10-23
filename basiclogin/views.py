from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm

from django.contrib.auth.decorators import login_required
from django.db import connection

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username,password)
            # Execute a raw SQL query to check the username and password
            with connection.cursor() as cursor:
                query = f"SELECT * FROM login.user WHERE name = '{username}' AND password = '{password}'"
                print(query)
                cursor.execute(query)
                user = cursor.fetchone()
                print("user", user)

            if user is not None:
                # Create a dummy user object or session (since you're not using Django's user model)
                # request.session['user_id'] = user[0]  # Assuming the first field is user ID
                # request.session['username'] = user[1]  # Assuming the second field is the username
                return redirect('dashboard')  # Redirect to the dashboard or another page
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


# @login_required
def dashboard(request):
    return render(request, 'dashboard.html')

def test_connection(request):
    from django.db import connection
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM login.user")
        results = cursor.fetchall()
    print('results', results)
    return render(request, 'users.html', {'results': results})

