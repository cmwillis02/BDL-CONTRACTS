from django.db import models
import uuid
from datetime import date
import datetime
from django.urls import reverse
from django.db.models import Sum, Count

# Create your models here.

class Contract(models.Model):
	"""
	Model representing Contract Fact
	"""

	player= models.ForeignKey('Player', on_delete= models.CASCADE, db_index=True, related_name = 'contract')
	franchise= models.ForeignKey('Franchise', on_delete= models.CASCADE, db_index= True, related_name = 'contract')
	current_ind= models.BooleanField()
	roster_status= models.CharField(max_length= 1, null= True)
	date_assigned= models.DateField()
	years= models.IntegerField(default= 0)
	years_remaining= models.IntegerField(null= True)
	date_terminated= models.DateField(null= True)
	
	def __str__(self):
		
		return '%s (%s)' % (self.player.name, self.franchise.team_name)
		
	def get_update_url(self):
		
		return reverse('update_contract', kwargs= {'pk' : self.pk})
	
	def get_detail_url(self):
		
		print (self.player_id)
		return reverse('player_contract_detail', kwargs= {'pk' : self.id})
	
	
class Franchise(models.Model):
	"""
	Model representing Franchise dimension
	"""
	
	franchise_id= models.IntegerField(primary_key= True)
	team_name= models.CharField(max_length= 50)
	owner_name= models.CharField(max_length= 50)
	owner_email= models.EmailField()
	
	def __str__(self):
	
		return self.team_name
		
	def get_absolute_url(self):
		
		return reverse('franchise_detail', args= [str(self.franchise_id)])
	
	#--- All get_<> methods are only for use in other methods, not in templates ---#
	def get_count(self, players):
	
		count= players.count()
		return count
	
	def get_years(self, players):
		
		years= players.aggregate(Sum('years_remaining'))
		return years['years_remaining__sum']
		
	def get_position_years(self, position):
		
		players= Contract.objects.filter(franchise_id= self.franchise_id).filter(current_ind= True).filter(player__position= position)
		years= self.get_years(players)
		
		return years
		
	def get_position_count(self, position):
		
		players= Contract.objects.filter(franchise_id= self.franchise_id).filter(current_ind= True).filter(player__position= position)
		count= self.get_count(players)
		
		return count
	
	#--- Methods to be used in templates and views ---#
	def total_years(self):
		
		players= Contract.objects.filter(franchise_id= self.franchise_id).filter(current_ind= True)
		years= self.get_years(players)
		
		return years
		
	def total_players(self):
		
		players= Contract.objects.filter(franchise_id= self.franchise_id).filter(current_ind= True)
		count= self.get_count(players)
		
		return count

	def qb_count(self):
		
		count= self.get_position_count('q')
		return count
	
	def qb_years(self):
		
		years= self.get_position_years('q')
		
		return years
		
	def rb_count(self):
		
		count= self.get_position_count('r')
		return count
	
	def rb_years(self):
		
		years= self.get_position_years('r')
		
		return years
		
	def wr_count(self):
		
		count= self.get_position_count('w')
		return count
	
	def wr_years(self):
		
		years= self.get_position_years('w')
		
		return years
		
	def te_count(self):
		
		count= self.get_position_count('t')
		return count
	
	def te_years(self):
		
		years= self.get_position_years('t')
		
		return years
		
	def def_count(self):
		
		count= self.get_position_count('d')
		return count
	
	def def_years(self):
		
		years= self.get_position_years('d')
		
		return years
		
	def k_count(self):
		
		count= self.get_position_count('k')
		return count
	
	def k_years(self):
		
		years= self.get_position_years('k')
		
		return years
		
		
	
class Player(models.Model):
	"""
	Model representing Player dimension
	"""
	
	player_id= models.IntegerField(primary_key= True)
	name= models.CharField(max_length= 50)
	
	Position= (
			('q', 'QB'),
			('r', 'RB'),
			('w', 'WR'),
			('t', 'TE'),
			('k', 'PK'),
			('d', 'DEF'),
			)
	
	position= models.CharField(max_length= 1, choices= Position)
	date_of_birth= models.DateField(null= True, blank= True)
	
	def __str__(self):
		
		return self.name
		

class Week(models.Model):
	"""
	Model representing Week Dimension table, used to define weeks as well as control update jobs
	"""
	
	week_id= models.IntegerField(primary_key= True)
	year= models.IntegerField()
	week= models.IntegerField()
	start_date= models.DateField()
	end_date= models.DateField()
	run_status= models.IntegerField()
	
	def __str__(self):
	
		return self.week_id