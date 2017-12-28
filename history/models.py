from django.db import models
from contracts.models import Player, Franchise
from django.urls import reverse

class player_fact(models.Model):
	"""
	Model representing player_fact table, one entry per player per week
	"""
	
	player= models.ForeignKey('contracts.Player', on_delete= models.CASCADE)
	week= models.ForeignKey('contracts.Week', on_delete= models.CASCADE)
	franchise= models.ForeignKey('contracts.Franchise', on_delete= models.CASCADE, null= True)
	
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
	
class franchise_fact(models.Model):
	"""
	Model representing franchise_fact, one entry per team per week
	"""
	
	franchise= models.ForeignKey('contracts.Franchise', on_delete= models.CASCADE)
	week= models.ForeignKey('contracts.Week', on_delete= models.CASCADE)
	opponent= models.ForeignKey('contracts.Franchise', on_delete= models.CASCADE, related_name= 'Franchise', null= True)
	
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
