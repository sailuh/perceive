
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
@csrf_protect
def home(request):
	if request.user.is_authenticated():
		#retrieve a start session or create new
		error_msg = ''
	        session_count = Session_log.objects.filter(user=request.user,session_action='_start')
		
		user_content_count = UserConsent.objects.filter(user=request.user).count()
		if user_content_count > 0:
			user_content = UserConsent.objects.filter(user=request.user)[user_content_count - 1]
		
		email_text1 = "Present random thread/knowledge source question Scenario:User should only be able to see this page upon successful authentication, which defines a session.One random e-mail thread and one associated knowledge source must be loaded into the questionnaire interface for the user to answer.In this scenario, the user interacts with the questionnaire interface through features 1,2 and 3 and the interaction is logged on the database as it is performed, so in case the user is interrupted / loss of connection / the session can be recovered, as well as the trace of the log.Only after All answers have been chosen, the user can submit the question. User should not be allowed to be presented other question otherwise, and the only means to move to the next presentation of e-mail thread/knowledge source is by submitting the answers (this ensures we dont have inconsistent answers all over the place. The questions allow for I dont knows so this is still safe).Once the user hits submit button, then the information of the questions is also stored, referring to the logs (note again: The logs should be stored as interactions are performed, so the schema needs to store questionaire answers and logs in separate tables so it can be stored in separate points in time). A new random e-mail thread and associated knowledge source is loaded and the scenario repeats.At any moment the user can click somewhere a log-off button or may lose connection. In both cases, the information should be reloaded from the interrupted session, but the next time the user logins / reestablish connection it should be considered a new session, albeit pointing to the same question / interaction log to the question. Concretely this means more than one session may point to the same question interaction log, which again requires the logs to be in separate tables.This the first email created for user: "+request.user.username
		e1 = EmailThread.objects.create(text_doc = email_text1)
		email_text2 = "Present random thread/knowledge source question Scenario:User should only be able to see this page upon successful authentication, which defines a session.One random e-mail thread and one associated knowledge source must be loaded into the questionnaire interface for the user to answer.In this scenario, the user interacts with the questionnaire interface through features 1,2 and 3 and the interaction is logged on the database as it is performed, so in case the user is interrupted / loss of connection / the session can be recovered, as well as the trace of the log.Only after All answers have been chosen, the user can submit the question. User should not be allowed to be presented other question otherwise, and the only means to move to the next presentation of e-mail thread/knowledge source is by submitting the answers (this ensures we dont have inconsistent answers all over the place. The questions allow for I dont knows so this is still safe).Once the user hits submit button, then the information of the questions is also stored, referring to the logs (note again: The logs should be stored as interactions are performed, so the schema needs to store questionaire answers and logs in separate tables so it can be stored in separate points in time). A new random e-mail thread and associated knowledge source is loaded and the scenario repeats.At any moment the user can click somewhere a log-off button or may lose connection. In both cases, the information should be reloaded from the interrupted session, but the next time the user logins / reestablish connection it should be considered a new session, albeit pointing to the same question / interaction log to the question. Concretely this means more than one session may point to the same question interaction log, which again requires the logs to be in separate tables.This the first email created for user: This the second email created for user: "+request.user.username
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

		elif request.method == 'POST' and 'end-session' in request.POST:
			check_session = Session_log.objects.filter(user=request.user).latest('time_action')
			if check_session.session_action == '_start':
				Session_log.objects.create(user = request.user, session_action = '_end') 
			else:
				error_msg = 'This session has already ended. LOgout and login to start a new session'

		elif request.method == "POST" and 'bheight' in request.POST:
        		#form = AdvertForm(request.POST)

		        #message = 'something wrong!'
		        #if(form.is_valid()):
			#print(request.POST['title'])
			log.debug(request.POST['bheight'])
            		bheight = request.POST['bheight']
			bwidth = request.POST['bwidth']
			bl = Box_log.objects.create(user = request.user,session = session, width = bwidth,height = bheight)
			log.debug(bheight)
        		#return HttpResponse(json.dumps({'bheight': bheight,'bwidth':bwidth}))
			return render(request,'home.html',{'user': request.user, 'session':session, 'user_content': user_content,'click_count':click_count, 'error_msg':error_msg,'bheight': bheight,'bwidth':bwidth})
		

		elif request.method == "POST" and 'scroll_pos' in request.POST:
        		
			log.debug(request.POST['scroll_pos'])
            		scroll_pos = request.POST['scroll_pos']
			
			sl = Box_scroll_log.objects.create(user = request.user,session = session, scrollbar_pos = scroll_pos)
			
        		#return HttpResponse(json.dumps({'bheight': bheight,'bwidth':bwidth}))
			return render(request,'home.html',{'user': request.user, 'session':session, 'user_content': user_content,'click_count':click_count, 'error_msg':error_msg,'scroll_pos': scroll_pos})

		#user_content.EmailThread.id = "does it exists?"
    	return render(request,'home.html',{'user': request.user, 'session':session, 'user_content': user_content,'click_count':click_count, 'error_msg':error_msg})

		
