from django.db import models
import uuid
from datetime import date
import datetime
from django.urls import reverse

# Create your models here.

class Contract(models.Model):
	"""
	Model representing Contract Fact
	"""

	player= models.ForeignKey('Player', on_delete= models.CASCADE, db_index=True, related_name = 'contract')
	franchise= models.ForeignKey('Franchise', on_delete= models.CASCADE, db_index= True, related_name = 'contract')
	current_ind= models.BooleanField()
	date_assigned= models.DateField()
	years= models.IntegerField(default= 0)
	years_remaining= models.IntegerField(null= True)
	date_terminated= models.DateField(null= True)
	
	def __str__(self):
		
		return '%s (%s)' % (self.player.name, self.franchise.team_name)
		
	def get_update_url(self):
		
		return reverse('update_contract', kwargs= {'pk' : self.pk})
	
		
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
		
class Player_fact(models.Model):
	"""
	Model representing player_fact table, one entry per player per week
	"""
	
	player= models.ForeignKey('Player', on_delete= models.CASCADE)
	week= models.ForeignKey('Week', on_delete= models.CASCADE)
	franchise= models.ForeignKey('Franchise', on_delete= models.CASCADE, null= True)
	
	roster_status= (
						('s','Starter'),
						('b','Bench'),
						('i','IR'),
						('f','Free Agent'),
						)
	roster_status= models.CharField(max_length= 50, choices= roster_status)
	score= models.FloatField(null= True)
	
	def __str__(self):
	
		return '%s (%s)' % (self.player.name, self.week.week_id)
	
class Franchise_fact(models.Model):
	"""
	Model representing franchise_fact, one entry per team per week
	"""
	
	franchise= models.ForeignKey('Franchise', on_delete= models.CASCADE)
	week= models.ForeignKey('Week', on_delete= models.CASCADE)
	opponent= models.ForeignKey('Franchise', on_delete= models.CASCADE, related_name= 'Franchise', null= True)
	
	matchup_type= (
			('p', 'Playoffs'),
			('r', 'Regular Season'),
			('b', 'Bye'),
			)
	
	matchup_type= models.CharField(max_length= 1, choices= matchup_type)
	
	result= (
				('w', 'Win'),
				('l', 'Loss'),
				('t', 'Tie'),
			)
	result= models.CharField(max_length= 1, choices= result, null= True)
	total_score= models.FloatField()
	opponent_score= models.FloatField(null= True)
	
	def __str__(self):
		
		return '%s (%s)' % (self.franchise.team_name, self.week.week_id)
	
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