from django.db import models
from django.contrib.auth.models import User
import datetime

class Tool (models.Model):

	def __unicode__(self):
		return self.toolType

	toolId = models.IntegerField()
	toolType = models.CharField(max_length=50)
	slug = models.SlugField(unique=True)
	#because a foreignkey can't be null, this is an integerfield pointing
	#to the shed_id of the shed in question.
	shed = models.IntegerField()
	owner = models.ForeignKey('ToolUser', related_name='owner')
	description = models.TextField(max_length = 200, blank=True)
	availability = models.IntegerField(default=1)
	homeLocation = models.CharField(max_length=60)
	zipCode = models.IntegerField()
	currentUser = models.ForeignKey('ToolUser',related_name='currentUser')

class ToolUser (models.Model):

	user = models.OneToOneField(User)
	name = models.CharField(max_length=25)
	address = models.CharField(max_length=100)
	zipCode = models.IntegerField()
	pickup = models.CharField(max_length=500, blank=True)
	banned = models.BooleanField(default=False)

	def __unicode__(self):
		return self.user.username 

class Shed(models.Model):

	def __unicode__(self):
		return self.name

	name = models.CharField(max_length=40)
	coordinator = models.ForeignKey('ToolUser', related_name='coordinator')
	motto = models.CharField(max_length=100)
	description = models.CharField(max_length=1000)
	zipCode = models.IntegerField()

class Update(models.Model):

	def __unicode__(self):
		return self.published

	subject = models.CharField(max_length=80)
	message = models.CharField(max_length=1000)
	published = models.CharField(max_length=10,default=""+str(datetime.datetime.now().month)+'-'+str(datetime.datetime.now().day)+'-'+str(datetime.datetime.now().year))

class Message(models.Model):

	def __unicode__(self):
		return "Message from "+self.sender.username+" to "+self.reciever.username

	sender = models.ForeignKey(User, related_name="sender")
	reciever = models.ForeignKey(User, related_name="reciever")
	subject = models.CharField(max_length=80)
	message = models.TextField(max_length=1000)
	date = models.CharField(max_length=10,default=""+str(datetime.datetime.now().month)+'-'+str(datetime.datetime.now().day)+'-'+str(datetime.datetime.now().year))

class SystemMessage(models.Model):

	def __unicode__(self):
		return "Message from the system to " + reciever.username + "regarding: "+subject

	reciever = models.ForeignKey(User)
	subject = models.CharField(max_length=80)
	message = models.CharField(max_length=1000)
	date = models.CharField(max_length=10,default=""+str(datetime.datetime.now().month)+'-'+str(datetime.datetime.now().day)+'-'+str(datetime.datetime.now().year))

class ToolRequest(models.Model):

	def __unicode__(self):
		return self.requester.name+" requests to borrow "+self.tool.owner.name+"'s "+self.tool.toolType

	requestId = models.IntegerField()
	tool = models.ForeignKey('Tool')
	requester = models.ForeignKey('ToolUser')
	date = models.CharField(max_length=10,default=""+str(datetime.datetime.now().month)+'-'+str(datetime.datetime.now().day)+'-'+str(datetime.datetime.now().year))
