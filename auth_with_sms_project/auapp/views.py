from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from .models import ProfileModel
from random import randrange

def usignup(request):
	if request.method == "POST":
		un = request.POST.get("un")
		ph = request.POST.get("ph")
		lo = request.POST.get("lo")
		try:
			usr = User.objects.get(username=un)
			return render(request, 'usignup.html', {'msg':'username already exists'})
		except User.DoesNotExist:
			try:
				usr = ProfileModel.objects.get(phone=ph)
				return render(request, 'usignup.html',{'msg':'phone number already exists'})
			except ProfileModel.DoesNotExist:
				pw = ""
				text = "1234567890"
				for i in range(6):
					pw = pw + text[randrange(len(text))]
				print(pw)
				send_sms(ph, pw)
				usr = User.objects.create_user(username=un, password=pw)
				usr.save()
				p = ProfileModel(phone=ph, location=lo, user=usr)
				p.save()
				return redirect('ulogin')
	else:
		return render(request, 'usignup.html')

def ulogin(request):
	if request.method == "POST":
		un = request.POST.get("un")
		pw = request.POST.get("pw")
		usr = authenticate(username=un, password=pw)
		if usr is None:
			return render(request, 'ulogin.html', {'msg':'bad credentials'})
		else:
			login(request, usr)
			return redirect('home')
	else:
		return render(request, 'ulogin.html')

def ulogout(request):
	logout(request)
	return redirect('ulogin')

def send_sms(ph, pw):
	import requests
	url = "https://www.fast2sms.com/dev/bulkV2"
	
	msg = "ur password is " + str(pw)
	
	querystring = {"authorization":"rpe8yIbwjHa7cWTC5149PiXfEhVBFzROvNx3QgSuoJsMqAK2GL7f1mBF6Jgc8AXboWTHE5U2MIkG3lKZ"
,"route" : "v3",
"sender_id" : "TXTIND",
"message" :msg,
"language" : "english",
"flash" : 0,
"numbers" : str(ph)}
	headers = {
		'cache-control': "no-cache"
	}
	response = requests.request("GET", url, headers=headers, params=querystring)

	print(response.text)

