from django.db import models

# Create your models here.

class Fact(models.Model):

	"""
	Model representing RFA_fact table.  Populated by <update> process.
	"""
	
	player_id(models.ForeignKey('contracts.player', on_delete= models.CASCADE))
	current_owner(models.ForeignKey('contracts.franchise', on_delete= models.CASCADE))
	franchise_tag(models.CharField(max_length=1))
	highest_bid(models.IntegerField())
	winning_owner(models.ForeignKey('contracts.franchise', on_delete= models.CASCADE, related_name='Franchise'))))
	match_status(models.CharField(max_length=1))
	week(models.ForeignKey('contracts.week', on_delete= models.CASCADE))
	transaction(models.IntegerField()) #place holder for when transaction foreign key is added
	
	def __str___(self):
	
		return "{} - {} RFA".format(self.player.name, self.franchise.team_name)