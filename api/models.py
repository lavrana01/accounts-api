from django.db import models

# Create your models here.
entry_type = (
    ("RECEIPT","Receipt"),
    ("PAYMENT","Payment")
)
class entries(models.Model):
    
    date = models.DateField(null=False)
    type_of_entry = models.CharField(max_length=100,choices=entry_type,default="None")
    particulars = models.TextField(max_length=200)
    detail = models.TextField(max_length= 200)
    amount = models.IntegerField(null=False)
    cash = models.IntegerField()

    def __str__(self):
        return self.particulars + " " + str(self.date)