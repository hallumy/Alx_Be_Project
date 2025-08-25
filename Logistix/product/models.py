from django.db import models

class Product(models.Model):
    code                = models.CharField(max_length=10)
    product_description = models.CharField(max_length=100, db_column='product_description')
    weight_kg          = models.FloatField(db_column='weight_kg')
    
    class Meta:
        db_table = 'product'
        
    def __str__(self):
        return f"{self.code} - {self.weight_kg}"
