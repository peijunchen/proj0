from django.http import HttpResponse
from django.template import Context, loader
from warmup.models import Users
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
import unittest
import StringIO
import json
from testAdditional import TestCase

SUCCESS               =   1  # : a success
ERR_BAD_CREDENTIALS   =  -1  # : (for login only) cannot find the user/password pair in the database
ERR_USER_EXISTS       =  -2  # : (for add only) trying to add a user that already exists
ERR_BAD_USERNAME      =  -3  # : (for add, or login) invalid user name (only empty string is invalid for now)
ERR_BAD_PASSWORD      =  -4

@csrf_exempt
def index(request):
	#TESTAPI_resetFixture() 
	if request.method == "POST":
		if request.path == "/TESTAPI/resetFixture":
			return TESTAPI_resetFixture()
		elif request.path == "/TESTAPI/unitTests":
			return TESTAPI_unitTest()
		elif request.path == "/users/login":	
			return login(request)
		elif request.path=="/users/add":
			return add(request)
		else:
			return
	elif request.method=="GET":
		if request.path not in ["/client.html","/client.css","/client.js"]:
			raise Http404
		else:
			mimeType="text/html"
			if request.path.endswith(".css"):
				mimeType = "text/css"
			elif request.path.endswith(".js"):
				mimeType = "text/javascript"
			return render_to_response('warmup'+request.path,{"message": "Please enter your credentials below"},mimetype=mimeType)
	

def ifExist(username):
	try:
		row = Users.objects.get(name = username)
		exist = True
	except:
		exist= False
		row = ""
	return (exist, row)

@csrf_exempt
def login(request):
#	username = password = ''
#	if request.POST:
#		username = request.POST.get('user')
#		password = request.POST.get('password')
#		
#		user = authenticate(username = username, password = password)
#		if user is not None:
#			if user.is_active:
#				login(request, user)
#				return HttpResponse(json.dumps({'errCode': SUCCESS, 'user': #inUserName, 'count': tempCount}),content_type="application/json" )
#			else: #account not active
#		else: #incorrect password
	inputData = json.loads(request.body)
	username, password = inputData["user"], inputData["password"]
	existance = ifExist(username)
	if existance[0] == True and existance[1].password == password:
		#handing the count
		existance[1].count+=1
		temp = existance[1].count
		existance[1].save()
		return HttpResponse(json.dumps({'errCode': SUCCESS, 'count': temp}),content_type="application/json" )
	else:
		return HttpResponse(json.dumps({'errCode': ERR_BAD_CREDENTIALS}),content_type="application/json" )

@csrf_exempt
def add(request):
	inputData = json.loads(request.body)
	username, newpassword = inputData["user"], inputData["password"]
	existance = ifExist(username)
	if existance[0] == True:
		return HttpResponse(json.dumps({'errCode': ERR_USER_EXISTS}),content_type="application/json" )
	elif username == "" or len(username)>128:
		return HttpResponse(json.dumps({'errCode': ERR_BAD_USERNAME}),content_type="application/json" )
       	elif len(newpassword)>128:
		return HttpResponse(json.dumps({'errCode': ERR_BAD_PASSWORD}),content_type="application/json" )
 	else:   
		row = Users(name=username, password = newpassword,count=1)
		row.save()
		return HttpResponse(json.dumps({'errCode': SUCCESS, "count":1}),content_type="application/json" )

def TESTAPI_resetFixture():
	Users.objects.all().delete()
	return HttpResponse(json.dumps({'errCode':SUCCESS}), content_type='application/json')

def TESTAPI_unitTest():
	temp_buffer = StringIO.StringIO()
	suite = unittest.TestLoader().loadTestsFromTestCase(Test)
	result = unittest.TextTestRunner(stream = temp_buffer, verbosity = 2).run(suite)
	rv = {"totalTests": result.testsRun, "nrFailed": len(result.failures), "output": temp_buffer.getvalue()}
	return HttpResponse(json.dumps(rv), content_type = "application/json")
	


		
