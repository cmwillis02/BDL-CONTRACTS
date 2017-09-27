from django.db import models
import uuid

# Create your models here.

class Contract(models.Model):
	"""
	Model representing Contract Fact
	"""

	player= models.ForeignKey('Player', on_delete= models.CASCADE, db_index=True)
	franchise= models.ForeignKey('Franchise', on_delete= models.CASCADE, db_index= True)
	current_ind= models.BooleanField()
	date_assigned= models.DateField()
	years= models.IntegerField(default= 0)
	date_terminated= models.DateField(null= True)
	
	def __str__(self):
		
		return '%s (%s)' % (self.player.name, self.franchise.team_name)
	
		
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
		
		return reverse('franchise-detail', args= [str(self.franchise_id)])
	
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
	
	