
#views.py
from loginapp.forms import *
from loginapp.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from random import sample
import logging 
log = logging.getLogger(__name__)

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
            )
            return HttpResponseRedirect('/register/success/')
    else:
        form = RegistrationForm()
    
 
    return render(request,'registration/register.html', {'form':form})
 
def register_success(request):
    return render_to_response('registration/success.html')
 
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')
 
@login_required
def home(request):
	if request.user.is_authenticated():
		#retrieve a start session or create new
		error_msg = ''
	        session_count = Session_log.objects.filter(user=request.user,session_action='_start')
		user_content_count = UserConsent.objects.filter(user=request.user).count()
		user_content = UserConsent.objects.filter(user=request.user)[user_content_count - 1]
		
		email_text1 = "This the first email created for user: "+request.user.username
		e1 = EmailThread.objects.create(text_doc = email_text1)
		email_text2 = "This the second email created for user: "+request.user.username
		e2 = EmailThread.objects.create(text_doc = email_text2)
		remail = sample([e1,e2],1)[0]
		if session_count.count() == 0:
				session = Session_log.objects.create(user = request.user, session_action = '_start')  
				source_doc = "This is the first knowledge source created for session id: "+str(session.id)
				ks = KnowledgeSource(source_doc=source_doc)
				ks.save()
				
				qs = Questions(answer = None , session=session)
				qs.save()
				user_content = UserConsent.objects.create(user=request.user,email_thread=remail,question=qs,knowledge_source=ks,session=session)
				click_count = Click_log.objects.filter(user=request.user,session=session).count()
				#content_create = 'true'			
			 
		else:
			log_session = Session_log.objects.filter(user=request.user).latest('time_action')
			if log_session.session_action == '_end':
	
				if request.method == 'POST' and 'end-session' in request.POST:
					error_msg = 'This session has already ended. LOgout and login to start a new session'
					session = log_session
					user_content = UserConsent.objects.filter(user=request.user,session=session)
					click_count = Click_log.objects.filter(user=request.user,session=session).count()
				else:
					session = Session_log.objects.create(user = request.user, session_action = '_start')
					source_doc = "This is the first knowledge source created for session id: "+str(session.id)
					ks = KnowledgeSource(source_doc=source_doc)
					ks.save()
					qs = Questions(answer = None , session=session)
					qs.save()
					user_content = UserConsent.objects.create(user=request.user,email_thread=remail,question=qs,knowledge_source=ks,session=session)
					click_count = Click_log.objects.filter(user=request.user,session=session).count()
					#content_create = 'true'
				
			else:
				session = log_session
				#user_content = UserConsent.objects.filter(user=request.user)
				user_content_count = UserConsent.objects.filter(user=request.user,session=session).count()
				user_content = UserConsent.objects.filter(user=request.user)[user_content_count - 1]
				click_count = Click_log.objects.filter(user=request.user,session=session).count()
				#content_create = 'false'
								
		
		
		#user_content = None
		#if content_create == 'true':
				
		#log.debug(user_content)
		#else:
				
		#log.debug(request.user)
		log.debug("print:")
		

		if request.method == 'POST' and 'hide-show' in request.POST:
			show_count = int(request.POST.get('disp_email'))
			if(show_count%2 == 0):
				show_action = "_show";
			else:
				show_action = "_hide";
			cl = Click_log.objects.create(user = request.user,session = session, click_action = show_action)

		if request.method == 'POST' and 'end-session' in request.POST:
			check_session = Session_log.objects.filter(user=request.user).latest('time_action')
			if check_session.session_action == '_start':
				Session_log.objects.create(user = request.user, session_action = '_end') 
			else:
				error_msg = 'This session has already ended. LOgout and login to start a new session'
		#user_content.EmailThread.id = "does it exists?"
    	return render(request,'home.html',{'user': request.user, 'session':session, 'user_content': user_content,'click_count':click_count, 'error_msg':error_msg})

		
