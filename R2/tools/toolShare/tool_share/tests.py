"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from tool_share.models import ToolUser
from tool_share.forms import *
from django.contrib.auth.models import User
#from django.contrib.auth import authenticate, login, logout
#from tool_share.forms import RegistrationForm, LoginForm, ToolRegistrationForm


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class viewsTests(TestCase):
	def setUp(self):
		self.client = Client()
		self.theUser = User.objects.create_user('John','email@host.com','test')
		#self.user = User.objects.create_user('John', 'email@host.com', 'test')

	def test_access_home(self):
		"""
		Tests if the index page is accesable
		"""
		resp = self.client.get('/newHome/')
		self.assertTemplateUsed(resp,'basenew.html')
		self.assertEqual(resp.status_code, 200)
		#self.assertContains(resp,'welcome',None,200,'',True)


	def test_access_login(self):
		"""
		Tests if the login page is accesable.
		"""
		resp = self.client.get('/login/')
		self.assertTemplateUsed(resp,'login.html')
		self.assertEqual(resp.status_code,200)
		#self.assertContains(resp.content,'created an account')

	def test_registration_page(self):
		"""
		Tests if the register page is accesable.
		"""
		resp = self.client.get('/register/')
		self.assertTemplateUsed(resp,'register.html')
		self.assertEqual(resp.status_code,200)

	def test_access_userspage(self):
		resp = self.client.get('/users/')
		self.assertTemplateUsed(resp,'users.html')
		self.assertEqual(resp.status_code,200)


	def test_access_shedspage(self):
		resp = self.client.get('/sheds/')
		self.assertTemplateUsed(resp,'sheds.html')
		self.assertEqual(resp.status_code,200)


	def test_access_messagespage(self):
		resp = self.client.get('/messagecenter/')
		self.assertTemplateUsed(resp,'message_center.html')
		self.assertEqual(resp.status_code,200)



	def test_login(self):
		"""
		Tests login redirection
		"""
		resp = self.client.post('/login/', {'username':'John','password':'test'})
		self.assertEqual(resp.status_code,302)
		#self.assertContains(resp.content,'Welcome back')

	def test_user_registration(self):
		"""
		Tests registration redirection
		"""
		resp = self.client.post('/register/',{'username':'test','email':'test@email.com','password':'test','passwordverify':'test'},follow=True)
		self.assertEqual(resp.status_code,200) #Not sure how to complete a registration in code
		#self.assertContains(resp.content)

	def test_tool_registration(self):
		"""
		Tests tool registration redirection
		"""
		resp = self.client.post('/registertool/',{'toolType':'wrench','description':'a wrench'},follow=True)
		self.assertEqual(resp.status_code,200)
		#self.assertContains(resp.content,'Full Name:')

	def test_shed_creation(self):
		return

	def test_sending_message(self):
		return



class modelTests(TestCase):

	def setUp(self):
		self.theUser = User.objects.create_user('John','email@host.com','test')
		self.testUser = ToolUser.objects.create(user=self.theUser,name='John',address='123 Street st.',zipCode=12345)

	def test_user_setup(self):
		"""
		Simple test setup tests
		"""
		self.assertEqual(self.testUser.name,'John')
		self.assertEqual(self.testUser.user,self.theUser)


class formTests(TestCase):

	def setUp(self):
		self.client = Client()
		self.theUser = User.objects.create_user('John','email@host.com','test')
	
	def test_login_forms(self):
		"""
		Tests if the login form accepts username and password strings
		"""
		form = LoginForm(data={'username': 'John','password': 'test'})
		self.assertTrue(form.is_valid())

	def test_bad_login_form(self):
		"""
		Tests if the login forms do not accept blank username and password strings.
		"""
		form = LoginForm(data={'username': '','password': 'test'}) #missing username
		self.assertFalse(form.is_valid())
		form = LoginForm(data={'username': 'John','password': ''}) #missing password
		self.assertFalse(form.is_valid())

	def test_registration_forms(self):
		form = RegistrationForm(data={'username':'John','email':'email@email.com',
			'password':'test','passwordverify':'test','fullname':'John','address':'123 street st','zipcode':'12345'})
		self.assertTrue(form.is_valid())

	def test_shed_form(self):
		"""
		Tests if a valid shed form is accepted
		"""
		form = ShedCreationForm(data={'name': 'myshed','motto': 'Is cool','description':'Did I mention its cool'})
		self.assertTrue(form.is_valid())

	def test_bad_shed_form(self):
		"""
		Tests if the shed form does not accept blank fields/
		"""
		form = ShedCreationForm(data={'name': '','motto': 'Is cool','description':'Did I mention its cool'}) #missing name
		self.assertFalse(form.is_valid())
		form = ShedCreationForm(data={'name': 'myshed','motto': '','description':'Did I mention its cool'})#missing motto
		self.assertFalse(form.is_valid())

	def test_tool_form(self):
		"""
		Tests if a valid tool form is accepted
		"""
		form = ToolRegistrationForm(data={'toolType':'hammer','description':'It hammers stuff'})
		self.assertTrue(form.is_valid())

	def test_bad_tool_form(self):
		form = ToolRegistrationForm(data={'toolType':'','description':'It hammers stuff'})#missing type
		self.assertFalse(form.is_valid())
		form = ToolRegistrationForm(data={'toolType':'hammer','description':''})
		self.assertFalse(form.is_valid())
		
class postTests(TestCase):

	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user('John', 'email@host.com', 'test')

