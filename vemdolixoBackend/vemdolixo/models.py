from __future__ import unicode_literals
from datetime import datetime
from django.db import models

# Create your models here.
class members(models.Model):
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	phone = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	newsletter_accepted_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	push_accepted_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	birthdate = models.DateTimeField(default=datetime.now)
	hash_id = models.CharField(max_length=200, default=None)
	username = models.CharField(max_length=200, default=None)
	email_activated = models.IntegerField(default=0)
	phone_activated = models.IntegerField(default=0)
	facebook_profile = models.CharField(max_length=400, default='')
	admin_level = models.IntegerField(default=0)
	profile_picture = models.CharField(max_length=400, default='https://s3-sa-east-1.amazonaws.com/residoando/user.svg')

	def __first_name__(self):
		return self.first_name

	def __last_name__(self):
		return self.last_name

	def __email__(self):
		return self.email

	def __phone__(self):
		return self.phone

	def __created_at__(self):
		return self.created_at

	def __newsletter_accepted_at__(self):
		return self.newsletter_accepted_at

	def __push_accepted_at__(self):
		return self.push_accepted_at

	def __birthdate__(self):
		return self.birthdate

	def __hash_id__(self):
		return self.hash_id

	def __username__(self):
		return self.username

	def __email_activated__(self):
		return self.email_activated

	def __phone_activated__(self):
		return self.phone_activated

	def __facebook_profile__(self):
		return self.facebook_profile

	def __admin_level__(self):
		return self.admin_level

class admin_codes(models.Model):
	code_hash = models.CharField(max_length=200, default=None)
	is_used = models.IntegerField(default=0)
	admin_level = models.IntegerField(default=2)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
	edited_at = models.DateTimeField(auto_now=True)

	def __code_hash__(self):
		return self.code_hash

	def __is_used__(self):
		return self.is_used

	def __admin_level__(self):
		return self.admin_level

	def __created_at__(self):
		return self.created_at

	def __edited_at__(self):
		return self.edited_at

class generic_register(models.Model):
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __first_name__(self):
		return self.first_name

	def __last_name__(self):
		return self.last_name

	def __email__(self):
		return self.email

class company(models.Model):
	organization_name = models.CharField(max_length=200)
	organization_type = models.CharField(max_length=200, default='')
	phone = models.CharField(max_length=200, default='')
	email = models.CharField(max_length=200, default='')
	city = models.CharField(max_length=200, default='')
	state = models.CharField(max_length=200, default='')
	neighborhood = models.CharField(max_length=200, default='')
	address = models.CharField(max_length=200, default='')
	website = models.CharField(max_length=200, default='')
	cnpj = models.CharField(max_length=200)
	latitude = models.DecimalField(max_digits=9, decimal_places=7)
	longitude = models.DecimalField(max_digits=9, decimal_places=7)
	is_active = models.IntegerField(default=1)
	description = models.CharField(max_length=400)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __organization_name__(self):
		return self.organization_name

	def __organization_type__(self):
		return self.organization_type

	def __phone__(self):
		return self.phone

	def __email__(self):
		return self.email

	def __city__(self):
		return self.city

	def __state__(self):
		return self.state

	def __neighborhood__(self):
		return self.neighborhood

	def __address__(self):
		return self.address

	def __website__(self):
		return self.website

	def __cnpj__(self):
		return self.cnpj

	def __latitude__(self):
		return self.latitude

	def __longitude__(self):
		return self.longitude

	def __is_active__(self):
		return self.is_active

	def __description__(self):
		return self.description

	def __created_at__(self):
		return self.created_at

class residue(models.Model):
	residue_name = models.CharField(max_length=200)
	unity = models.CharField(max_length=200)

	def __residue_name__(self):
		return self.residue_name

	def __unity__(self):
		return self.unity

class residue_association(models.Model):
	term = models.CharField(max_length=200)
	residue_id = models.IntegerField(default=0)

	def __term__(self):
		return self.term

	def __residue_id__(self):
		return self.residue_id

class receptivity(models.Model):
	residue_id = models.IntegerField(default=0)
	company_id = models.IntegerField(default=0)
	minimun = models.IntegerField(default=0)
	maximun = models.IntegerField(default=0)
	is_active = models.IntegerField(default=1)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __residue_id__(self):
		return self.residue_id

	def __company_id__(self):
		return self.company_id

	def __minimun__(self):
		return self.minimun

	def __maximun__(self):
		return self.maximun

	def __is_active__(self):
		return self.is_active

	def __created_at__(self):
		return self.created_at

class search_history(models.Model):
	text = models.CharField(max_length=200)
	member_id = models.IntegerField(default=0)
	latitude = models.DecimalField(max_digits=9, decimal_places=7)
	longitude = models.DecimalField(max_digits=9, decimal_places=7)
	created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __text__(self):
		return self.text

	def __member_id__(self):
		return self.member_id

	def __latitude__(self):
		return self.latitude

	def __longitude__(self):
		return self.longitude

	def __created_at__(self):
		return self.created_at