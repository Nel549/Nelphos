from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterUserForm, ContanctForm

#email
#from sendgrid import SendGridAPIClient
#from sendgrid.helpers.mail import Mail
from presets.models import Preset

# Create your views here.

def home(request):
    presets = Preset.objects.all()[:4]

    return render(request, 'base/home.html', {'presets': presets})

def about(request):
    return render(request, 'base/about.html')

def contact(request):
    form = ContanctForm()

    if request.method == 'POST':
        form = ContanctForm(request.POST)

        if form.is_valid():
            pass
            #I was sending emails using sendgrid API.
            '''
            name = request.POST['name']
            sender_email = request.POST['email']
            message = request.POST['message']

            email_template_name = 'base/contact.txt'
            parameters = {
                'name': name,
                'email': sender_email,
                'msg': message,
            }
            email = render_to_string(email_template_name, parameters)

            message = Mail(
            from_email='email',
            to_emails='email',
            subject='Someone wants to contact you!',
            html_content=email)
            try:
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                response = sg.send(message)

                print(response.status_code)
                print(response.body)
                print(response.headers)
                return redirect('home')
            except Exception as e:
                print(f"Error here {e}")
            '''
            
        

    return render(request, 'base/contact.html', {'form': form})

def login_user(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            #succes
            login(request, user)
            return redirect('profiles', username)
        else:
            pass

    context = {}

    return render(request, 'base/login.html', context)

def register(request):
    form = RegisterUserForm()

    if request.method == 'POST':
        form = RegisterUserForm(request.POST)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.save()

            login(request,new_user)
            return redirect('profiles', request.POST['username'])



    context = {'form': form}

    return render(request, 'base/register.html', context)

def logout_user(request):
    logout(request)
    return redirect('home')