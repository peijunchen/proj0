from django.utils  import unittest
import os
import testLib
        

SUCCESS               =   1  # : a success
ERR_BAD_CREDENTIALS   =  -1  # : (for login only) cannot find the user/password pair in the database
ERR_USER_EXISTS       =  -2  # : (for add only) trying to add a user that already exists
ERR_BAD_USERNAME      =  -3  # : (for add, or login) invalid user name (only empty string is invalid for now)
ERR_BAD_PASSWORD      =  -4

class TestCase(testLib.RestTestCase):
    	"""Test adding users"""
	def assertResponse(self, respData, count = 1, errCode = testLib.RestTestCase.SUCCESS):
        	"""
        	Check that the response data dictionary matches the expected values
        	"""
        	expected = { 'errCode' : errCode }
        	if count is not None:
            		expected['count']  = count
        	self.assertDictEqual(expected, respData)
       
   	def testGoodAdd(self):
        	respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'})
        	self.assertResponse(respData, 1, testLib.RestTestCase.SUCCESS)
	def testGoodADD_EmptyPassword(self):
		respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : ''})
		self.assertResponse(respData, 1, testLib.RestTestCase.SUCCESS)
	def testBadAdd_EmptyName(self):
        	respData = self.makeRequest("/users/add", method="POST", data = { 'user' : '', 'password' : 'password'} )
        	self.assertResponse(respData, None, testLib.RestTestCase.ERR_BAD_USERNAME)
	def testBadAdd_NameToolong(self):
        	respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1'*100, 'password' : 'password'} )
        	self.assertResponse(respData, None, testLib.RestTestCase.ERR_BAD_USERNAME)
	def testBadAdd_PasswordToolong(self):
        	respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'*100} )
        	self.assertResponse(respData, None, testLib.RestTestCase.ERR_BAD_PASSWORD)
	def testBadAdd_NameExist(self):
        	self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        	respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        	self.assertResponse(respData, None, testLib.RestTestCase.ERR_USER_EXISTS)
	def testGoodLogin(self):
        	self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        	respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        	self.assertResponse(respData, 2, testLib.RestTestCase.SUCCESS)
	def testBadLogin_WrongPassword(self):
		self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        	respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user1', 'password' : 'passwords'} )
        	self.assertResponse(respData, None, testLib.RestTestCase.ERR_BAD_CREDENTIALS)
	def testBadLogin_WrongUsername(self):
		self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        	respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user2', 'password' : 'password'} )
        	self.assertResponse(respData, None, testLib.RestTestCase.ERR_BAD_CREDENTIALS)
	def testBadLogin_NameToolong(self):
        	respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user1'*100, 'password' : 'password'} )
        	self.assertResponse(respData, None, testLib.RestTestCase.ERR_BAD_CREDENTIALS)
	def testBadLogin_PasswordToolong(self):
        	respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user1', 'password' : 'password'*100} )
        	self.assertResponse(respData, None, testLib.RestTestCase.ERR_BAD_CREDENTIALS)



