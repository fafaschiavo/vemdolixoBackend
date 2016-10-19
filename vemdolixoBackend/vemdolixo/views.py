# -*- coding: utf-8 -*-
import sys
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.conf import settings
from vemdolixo.models import generic_register, company, residue, receptivity, search_history, members, admin_codes, residue_association
from django.http import HttpResponse
from difflib import SequenceMatcher
import json
import csv
import googlemaps
from datetime import datetime
import re
import decimal
import string
import random
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db import connection

# Create your procedures here

def convert_characters(string_to_convert):
	reload(sys)
	sys.setdefaultencoding('UTF8')
	converted_string = string_to_convert
	converted_string = converted_string.replace("Ã§", "ç")
	converted_string = converted_string.replace("Ã£", "ã")
	converted_string = converted_string.replace("Ã¡", "á")
	converted_string = converted_string.replace("Ã©", "é")
	converted_string = converted_string.replace("Ãº", "ú")
	converted_string = converted_string.replace("Ã³", "ó")
	converted_string = converted_string.replace("Ã´", "ô")
	converted_string = converted_string.replace("Ã", "í")
	return converted_string

def rank_string_similarity_with_residues_type(string_to_test):
	residues = residue_association.objects.all()
	match_array = {}
	for residue_type in residues:
		result = SequenceMatcher(None, string_to_test, residue_type.term).ratio()
		original_residue = residue.objects.filter(id = residue_type.residue_id)
		match_array[result] = original_residue

	score_array = sorted(match_array, reverse=True)

	result_array = {}
	index = 0
	for score in score_array:
		result_array[index] = match_array[score][0]
		index = index + 1

	return result_array

def rank_string_similarity(string_to_test):
	residues = residue_association.objects.all()
	match_array = {}
	for residue_type in residues:
		result = SequenceMatcher(None, string_to_test, residue_type.term).ratio()
		original_residue = residue.objects.filter(id = residue_type.residue_id)
		match_array[result] = original_residue

	score_array = sorted(match_array, reverse=True)
	
	return score_array

def hash_id_generator(size=10, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def generate_member_hash_id():
	verify_existence = True
	while verify_existence == True:
		new_hash_id = hash_id_generator()
		try:
			member = members.objects.all(hash_id = new_hash_id)
		except:
			verify_existence = False
	return new_hash_id

def verify_admin_code(admin_code):
	verify = False
	try:
		code_object = admin_codes.objects.get(code_hash = admin_code)
		if code_object.is_used == 0:
			verify = code_object.admin_level
	except:
		pass
	return verify

def consume_admin_code(admin_code):
	code_object = admin_codes.objects.get(code_hash = admin_code)
	code_object.is_used = 1
	code_object.save()
	return True

# Create your views here.

def new_member(request):
	context = {}
	return render(request, 'new-member.html', context)

def create_new_member(request):
	context = {}
	firstname = request.POST['firstname']
	lastname = request.POST['lastname']
	email = request.POST['email']
	username = request.POST['username']
	password = request.POST['password']
	admin_code = request.POST['admin_code']

	hash_id = generate_member_hash_id()
	admin_verification = verify_admin_code(admin_code)

	if admin_verification != False:
		new_member = members(first_name = firstname, last_name = lastname, email = email, hash_id = hash_id, username = username, admin_level = admin_verification)
		new_member.save()
		user = User.objects.create_user(username = username, first_name = firstname, last_name = lastname, email = email, password = password)
		user.save()
		consume_admin_code(admin_code)
	else:
		return HttpResponse ('Erro no código de administrador')


	return render(request, "login.html", context)

def login_page(request):
	context = {}
	return render(request, 'login.html', context)

def login_user(request):
	context = {}
	username = request.POST['username']
	password = request.POST['password']
	auth_user = authenticate(username=username, password=password)
	if auth_user is not None:
	    if auth_user.is_active:
	        result = members.objects.filter(username = username)
	        user = result[0]
	        if user.admin_level>0:
	            login(request, auth_user)
	            companies = company.objects.all()
	            company_index = {}
	            for company_item in companies:
	        	    company_index[company_item] = company_item
	            context = {
	        	    'company_index': company_index,
	        	    'first_name': user.first_name
	            }
	            return render(request, 'index.html', context)
	        else:
	            return HttpResponse ('Você não tem permissão para acessar esse sistema')
	    else:
	        return HttpResponse ('Usuario nao ativo')
	else:
	    return HttpResponse ('Usuario ou senha incorretos')

def logout_user(request):
	logout(request)
	context = {}
	return render(request, "login.html", context)

@login_required
def index(request):
	username = request.user
	result = members.objects.filter(username = username)
	user = result[0] 

	companies = company.objects.all()
	company_index = {}
	for company_item in companies:
		company_index[company_item] = company_item

	context = {
		'user_email': user.email,
		'user_picture': user.profile_picture,
		'user_name': user.first_name,
		'company_index': company_index,
	}
	return render(request, 'index.html', context)

@login_required
def companies_page(request):
	username = request.user
	result = members.objects.filter(username = username)
	user = result[0]

	with connection.cursor() as cursor:
		cursor.execute("select organization_type from vemdolixo_company group by organization_type;")
		organization_types = cursor.fetchall()

	autocomplete_type = ''
	for organization_type in organization_types:
		autocomplete_type = autocomplete_type + "'" + convert_characters(organization_type[0]) + "',"

	with connection.cursor() as cursor:
		cursor.execute("select city from vemdolixo_company group by city;")
		cities = cursor.fetchall()

	autocomplete_city = ''
	for city in cities:
		autocomplete_city = autocomplete_city + "'" + convert_characters(city[0]) + "',"

	with connection.cursor() as cursor:
		cursor.execute("select state from vemdolixo_company group by state;")
		states = cursor.fetchall()

	autocomplete_state = ''
	for state in states:
		autocomplete_state = autocomplete_state + "'" + convert_characters(state[0]) + "',"

	with connection.cursor() as cursor:
		cursor.execute("select neighborhood from vemdolixo_company group by neighborhood;")
		neighborhoods = cursor.fetchall()

	autocomplete_neighborhood = ''
	for neighborhood in neighborhoods:
		autocomplete_neighborhood = autocomplete_neighborhood + "'" + convert_characters(neighborhood[0]) + "',"

	companies = company.objects.all()
	company_index = {}
	for company_item in companies:
		company_index[company_item] = company_item

	context = {
		'user_email': user.email,
		'user_picture': user.profile_picture,
		'user_name': user.first_name,
		'company_index': company_index,
		'tags_type': autocomplete_type,
		'tags_city': autocomplete_city,
		'tags_state': autocomplete_state,
		'tags_neighborhood': autocomplete_neighborhood,
	}
	return render(request, 'companies.html', context)

def new_company(request):
	company_name = request.POST['company_name']
	company_type = request.POST['company_type']
	phone = request.POST['phone']
	email = request.POST['email']
	city = request.POST['city']
	state = request.POST['state']
	neighborhood = request.POST['neighborhood']
	address = request.POST['address']
	website = request.POST['website']
	cnpj = request.POST['cnpj']
	latitude = request.POST['latitude']
	longitude = request.POST['longitude']

	try:
		new_company = company(organization_name = company_name,
			organization_type = company_type,
			phone = phone,
			email = email,
			city = city,
			state = state,
			neighborhood = neighborhood,
			address = address,
			website = website,
			cnpj = cnpj,
			latitude = latitude,
			longitude = longitude,
			)
		new_company.save()
		return HttpResponse ('Cadastro feito com sucesso')
	except:
		return HttpResponse ('Falha ao cadastrar')

def new_company_csv(request):
	if request.POST and request.FILES:
		csvfile = request.FILES['csv_file']
		# dialect = csv.Sniffer().sniff(codecs.EncodedFile(csvfile, "utf-8").read(1024))
		csvfile.open()
		# spamreader = csv.reader(csvfile, encoding='utf-8', delimiter='&', quotechar='|')
		spamreader = csv.reader(csvfile, delimiter='&', quotechar='|')
		success = 0
		failure = 0
		for row in spamreader:
			try:
				new_company = company(organization_name = row[1],
					organization_type = row[0],
					phone = row[2] ,
					email = row[3],
					city = row[4],
					state = row[5],
					neighborhood = row[6],
					address = row[7],
					website = row[8],
					cnpj = row[9],
					latitude = row[10],
					longitude = row[11],
					)
				new_company.save()
				success = success + 1
			except:
				failure = failure + 1
		return HttpResponse("Envios bem sucedidos - " + str(success) + " | Falhas no envio - " + str(failure))
	else:
		return HttpResponse('Problemas com seu arquivo')

def receptivity_page(request):
	residues = residue.objects.all()
	residue_index = {}
	for residue_item in residues:
		residue_index[residue_item] = residue_item

	context = {
	'residue_index': residue_index,
	}
	return render(request, 'receptivity.html', context)

def new_receptivity_entry(request):
	residue_id = request.POST['residue_id']
	company_id = request.POST['company_id']
	minimun = request.POST['minimun']
	maximun = request.POST['maximun']

	try:
		new_receptivity = receptivity(residue_id = residue_id,
			company_id = company_id,
			minimun = minimun,
			maximun = maximun,
			)
		new_receptivity.save()
		return HttpResponse ('Cadastro feito com sucesso')
	except:
		return HttpResponse ('Falha ao cadastrar')

@login_required
def dashboard(request):
	username = request.user
	result = members.objects.filter(username = username)
	user = result[0]

	with connection.cursor() as cursor:
		cursor.execute("select count(*), date(created_at) from vemdolixo_search_history group by date(created_at);")
		search_history_per_date = cursor.fetchall()

	search_series_to_chart = "'"
	search_amount_to_chart = ""
	search_total_to_chart = ""
	search_total = 0
	for search in search_history_per_date:
		search_series_to_chart = search_series_to_chart + str(search[1]) + "', '"
		search_amount_to_chart = search_amount_to_chart + str(search[0]) + ", "
		search_total = search_total + search[0]
		search_total_to_chart = search_total_to_chart + str(search_total) + ", "
	search_series_to_chart = search_series_to_chart[:-3]
	search_amount_to_chart = search_amount_to_chart[:-2]
	search_total_to_chart = search_total_to_chart[:-2]

	with connection.cursor() as cursor:
		cursor.execute("select count(*), date(created_at) from (select * from vemdolixo_generic_register group by email) as A group by date(created_at);")
		email_register_per_date = cursor.fetchall()

	register_series_to_chart = "'"
	register_amount_to_chart = ""
	register_total_to_chart = ""
	register_total = 0
	for register in email_register_per_date:
		register_series_to_chart = register_series_to_chart + str(register[1]) + "', '"
		register_amount_to_chart = register_amount_to_chart + str(register[0]) + ", "
		register_total = register_total + register[0]
		register_total_to_chart = register_total_to_chart + str(register_total) + ", "
	register_series_to_chart = register_series_to_chart[:-3]
	register_amount_to_chart = register_amount_to_chart[:-2]
	register_total_to_chart = register_total_to_chart[:-2]

	context = {
		'user_email': user.email,
		'user_picture': user.profile_picture,
		'user_name': user.first_name,
		'search_series_to_chart': search_series_to_chart,
		'search_amount_to_chart': search_amount_to_chart,
		'search_total_to_chart': search_total_to_chart,
		'register_series_to_chart': register_series_to_chart,
		'register_amount_to_chart': register_amount_to_chart,
		'register_total_to_chart': register_total_to_chart,
	}
	return render(request, 'overview.html', context)

@login_required
def search_map(request):
	username = request.user
	result = members.objects.filter(username = username)
	user = result[0]

	searches = search_history.objects.all()

	context = {
		'user_email': user.email,
		'user_picture': user.profile_picture,
		'user_name': user.first_name,
		'searches': searches,
	}
	return render(request, 'search-map.html', context)

@login_required
def residues(request):
	username = request.user
	result = members.objects.filter(username = username)
	user = result[0]

	context = {
		'user_email': user.email,
		'user_picture': user.profile_picture,
		'user_name': user.first_name,
	}
	return render(request, 'similarity-rank.html', context)

def similarity_rank_result(request):
	username = request.user
	result = members.objects.filter(username = username)
	user = result[0]

	string_to_match = request.GET['string_to_rank']

	result_array = rank_string_similarity_with_residues_type(string_to_match)
	score_array = rank_string_similarity(string_to_match)
	result_array_to_table = []
	for result in result_array:
		result_array_to_table.append(result_array[result].residue_name)

	context = {
		'user_email': user.email,
		'user_picture': user.profile_picture,
		'user_name': user.first_name,
		'result_array_to_table': result_array_to_table,
		'score_array_to_table': score_array,
	}
	return render(request, 'similarity-rank-result.html', context)

@login_required
def machine_learning_advisor(request):
	username = request.user
	result = members.objects.filter(username = username)
	residues = residue.objects.all()
	searches = search_history.objects.all()
	user = result[0]

	uncategorized = {}
	for search in searches:
		score_array = rank_string_similarity(search.text)
		if score_array[0] <  0.57:
			reload(sys)
			sys.setdefaultencoding('UTF8')
			uncategorized[search.text] = score_array[0]

	context = {
		'user_email': user.email,
		'user_picture': user.profile_picture,
		'user_name': user.first_name,
		'uncategorized': uncategorized,
		'residues': residues,
	}
	return render(request, 'machine-learning-advisor.html', context)

def machine_learning_associoation(request):
	residue_id = request.GET['residue_id']
	term = request.GET['term']

	try:
		association = residue_association.objects.get(term = term)
		association.residue_id = residue_id
		association.save()
	except:
		association = residue_association(term = term, residue_id = residue_id)
		association.save()

	return HttpResponse(200)