from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
#from decorator import view_new_notification
from django.contrib.auth.models import User
from forms import UserForm, CreateProjectForm, FilterForm, SolutionForm
from models import Projects, Solution, Notifications

### CUSTOM FUNCTIONS
import uuid
def genid(prefix):
	return prefix+str(uuid.uuid4())

def is_a_num(s):
	try:
		float(s)
		return True
	except ValueError:
		return False

def create_notification(username, link, title):
	Notifications.objects.create(username=username, link=link, title=title)

def remove_notification(remove_notification_title):
	noti =Notifications.objects.get(title=remove_notification_title)
	noti.is_new = False
	noti.save()

def notifications(request):
	user = request.user.username
	notifications = {}
	notifications["nots"] = []
	for noti in Notifications.objects.filter(username=user):
		if noti.is_new:
			notifications["nots"].append({"link":noti.link,"title":noti.title})
	
	if notifications["nots"] != []:
		notifications["is_new"] = True
	else:
		notifications["is_new"] = False
	notifications["number"] = str(len(notifications["nots"]))
	return notifications



### MAPPED FUNCTIONS
def register(request):

	error_msg = False

	if request.method == 'POST':

		error_msg = []

		uf = UserForm(request.POST, prefix='user')
		#print User.objects.all()
		if request.POST.get('user-password1') != request.POST.get('user-password2'):
			error_msg.append("Password do not match")
		if len(request.POST.get('user-password1')) < 8 or len(request.POST.get('user-password1')) > 75:
			error_msg.append("Password must be between 8 and 75 characthers")
		try:
		 	username_error = User.objects.get(username=request.POST.get('user-username'))
		 	error_msg.append("Username is taken")
		except User.DoesNotExist:
			pass

		if uf.is_valid():

				#user = uf.save(commit=False)
				user = uf.save(commit=True)
				new_user = User.objects.get(username=request.POST.get('user-username'))
				new_user.userprofile.balance = 0
				new_user.userprofile.is_admin = False
				
				#user.userprofile.balance = 0
				#user.userprofile.is_admin = False
#
				new_user.save()
				return HttpResponseRedirect("/success")

	else:

		uf = UserForm(prefix='user')

	return render(request,"BuildPythonPleaseGUI/register.html", {
			"userform":uf,
			"error_msg":error_msg,
			})

def success(request):

	return render(request, 'BuildPythonPleaseGUI/success.html')

def terms_and_conditions(request):

	return render(request, 'BuildPythonPleaseGUI/terms_and_conditions.html', {'notifications':notifications(request)})

#@login_required(login_url="login")
def home(request):

	return render(request,"BuildPythonPleaseGUI/home.html", {
			'notifications':notifications(request),
			})


def about_us(request):
	#print UserProxy
	#print request
	#create_notification(request.user.username, "/", "Visited About Us page")
	return render(request, 'BuildPythonPleaseGUI/about_us.html', {'notifications':notifications(request)})
	#return render(request, 'BuildPythonPleaseGUI/about_us.html')

@login_required(login_url="login")
def projects(request):

	form = FilterForm()
	if request.method == 'POST':
		form = FilterForm(request.POST)
		# DOESNT WORK without print statement?????
		print form
		search = form.clean().get("search")

		if search == 'Open Projects':
			projects = Projects.objects.filter(status="Open")
			search_title = "Available Projects"

		elif search == 'Closed Projects':
			projects = Projects.objects.filter(status="Closed")
			search_title = "Closed Projects"

		elif search == 'My Projects':
			projects = Projects.objects.filter(owner=request.user.username)
			search_title = "My Projects"

		elif search == "All Projects":
			projects = Projects.objects.all()
			search_title = "All Projects"
	else:
		projects = Projects.objects.filter(status="Open")
		search_title = "Available Projects"


	return render(request, 'BuildPythonPleaseGUI/projects.html', {
			"search_title":search_title,
			"projects":projects,
			"form":form, 
			'notifications':notifications(request)
		})

@login_required(login_url="login")
def create_project(request):
	form = CreateProjectForm()
	if request.method == 'POST':
		title = request.POST.get("title")
		owner = request.user.username
		version = request.POST.get("version")
		client = request.POST.get("client")
		description = request.POST.get("description")
		status = "Open"
		payout = request.POST.get("payout")

		projects = Projects(title=title, owner=owner, version=version, client=client, description=description, status=status, payout=payout)
		
		if is_a_num(request.POST.get("payout")):

			if int(request.POST.get("payout")) <= int(User.objects.get(username=owner).userprofile.balance):
				new_balance  = int(User.objects.get(username=owner).userprofile.balance) - int(request.POST.get("payout"))
				user = User.objects.get(username=owner)
				user.userprofile.balance = new_balance
				#update balance
				user.save()

				#add project
				projects.save()

				return HttpResponseRedirect("/projects/")

			else:

				return render(request, 'BuildPythonPleaseGUI/create_project.html', {
				"form":CreateProjectForm(initial={"title":title,
												"version":version,
												"client":client,
												"description":description,
												}),
											"form_error":True,
											})

			
		else:

			return render(request, 'BuildPythonPleaseGUI/create_project.html', {
				"form":CreateProjectForm(initial={"title":title,
												"version":version,
												"client":client,
												"description":description,
												"payout":payout
												}),
											"form_error":True,
										})
	else:
		

		return render(request, 'BuildPythonPleaseGUI/create_project.html', {
				"form":form,
				"form_error":False, 
				'notifications':notifications(request),
			})

@login_required(login_url="login")
def project(request, id):
	project = Projects.objects.get(id=id)
	user = User.objects.get(username=request.user.username)

	remove_notification_title = request.GET.get("remove_notification")
	if remove_notification_title != None:
		remove_notification(remove_notification_title)

	if project.owner == request.user.username:	is_owner = True
	else:	is_owner = False

	if project.status == "Closed":	is_closed = True
	else: is_closed = False

	if request.GET.get('Close') == "Close Project":
		if project.status == "Open" and is_owner:
			Projects.objects.select_related().filter(id=project.id).update(status="Closed")
			user.userprofile.balance = int(user.userprofile.balance) + int(project.payout)
			user.save()
			return HttpResponseRedirect("/projects/")

	elif request.GET.get('submit_solution') == "Submit Solution":
		form = SolutionForm()
		return render(request, 'BuildPythonPleaseGUI/project_solution.html', {
												"project":project,
												"form":form,
												"id":id,
												'notifications':notifications(request),
												})

	elif request.GET.get('accept_solution') == "Accept Solution":
		if project.status == "Open":
			solution_id = request.GET.get('solution_id')
			sol = Solution.objects.get(id=solution_id)
			#update senders balance
			user = User.objects.get(username=sol.sender)
			new_balance = str(int(user.userprofile.balance) + int(project.payout))
			user.userprofile.balance = new_balance
			user.save()
	
			#closed project
			project.status = "Closed"
			project.save()

			create_notification(sol.sender, "/project/"+id+"/", "Solution accepted for "+project.id+" with "+sol.id+" - "+project.payout+" added to balance")
			
			for sol_in_proj in Solution.objects.filter(project_id=sol.project_id):
				sol_in_proj.delete()
				create_notification(sol_in_proj.sender, "/project/"+id+"/", sol.id+" declined for "+project.id)
			return HttpResponseRedirect("/projects/")

	elif request.GET.get('decline') == "Decline":
		solution_id = request.GET.get('solution_id')
		sol =Solution.objects.get(id=solution_id)

		create_notification(sol.sender, "/project/"+id+"/", sol.id+" declined for "+project.id)
		sol.delete()
		
		return HttpResponseRedirect("/project/"+id+"/")

	if is_owner:
		solutions = []

		for sol in Solution.objects.filter(project_id=id):
			solutions.append(sol)
		
		if len(solutions) > 0:
			return render(request, 'BuildPythonPleaseGUI/project.html', {
										"project":project,
										"is_owner":is_owner,
										"is_closed":is_closed,
										"solutions":solutions,
										'notifications':notifications(request),
										})

	if request.method == 'POST':

		sf = SolutionForm(request.POST)

		#print request.POST

		if sf.is_valid():

			solution = sf.save(commit=False)
			solution.id = genid("Solution:")
			solution.owner = project.owner
			solution.sender = user.username
			solution.project_id = id
			solution = sf.save(commit=True)

			create_notification(project.owner, "/project/"+id+"/#"+solution.id, "New Solution - "+solution.id)
			#for sol in Solution.objects.all():	print sol.solution


	return render(request, 'BuildPythonPleaseGUI/project.html', {
												"project":project,
												"is_owner":is_owner,
												"is_closed":is_closed,
												"solutions":False,
												'notifications':notifications(request),
												})


@login_required(login_url="login")
def all_users(request):
	#warning can change request.user
	#look how to use session id
	#same issue in messages, projects, create_project and project, notifications
	user = User.objects.get(username=request.user.username)
	#print user
	#is_admin = user.userprofile.is_admin
	if user.userprofile.is_admin:
		every_user = User.objects.all()
		
		if request.GET.get('delete_user') == "Delete User":
			user =  request.GET.get("username")
			User.objects.get(username=user).delete()

		return render(request, 'BuildPythonPleaseGUI/all_users.html', {
													"every_user":every_user,
													'notifications':notifications(request),
													})
	return render(request, "BuildPythonPleaseGUI/all_users.html", { 
													'notifications':notifications(request),
													})

def messages(request):
	user = User.objects.get(username=request.user.username)
	
	user_notifications = Notifications.objects.filter(username=user)
	if request.GET.get("notification_id") != None and request.GET.get("delete")=="Delete":
		notification = Notifications.objects.get(id=request.GET.get("notification_id"))
		if notification.username == user.username:
			notification.delete()

	elif request.GET.get("delete_all")=="Delete All":
		user_notifications.delete()
		
	user_notifications.update(is_new=False)
	return render(request, "BuildPythonPleaseGUI/messages.html", { 
													'notifications':notifications(request),
													'user_notifications':user_notifications,
													})