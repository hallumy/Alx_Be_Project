from django.db import models

class Product(models.Model):
    code        = models.CharField(max_length=10, unique=True)
    product_description = models.CharField(max_length=100, db_column='product description')
    weight_kgs      = models.FloatField(db_column='weight(kgs)')
    
    class Meta:
        db_table = 'products'
        managed = False
        
    def __str__(self):
        return f"{self.code} - {self.description[:30]}"

