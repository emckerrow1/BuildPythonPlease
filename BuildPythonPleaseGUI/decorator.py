from django.shortcuts import render

#test
def view_new_notification(view_func):
	def wrapper(request, *args, **kwargs):
		r = view_func(request, *args, **kwargs)
		r.context_data = {'foo': 'bar'}
		return r.render()
	return wrapper