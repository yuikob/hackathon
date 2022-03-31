from django.db import models

class Pochi(models.Model):
    class Meta:
        db_table = "pochi"
        verbose_name = "ぽちぽち"
        verbose_name_plural = "ぽちぽち"

    hsd_data = models.FileField(
        upload_to='uploads/',
        default='',
    )

    rgb_base64 = models.TextField(
        verbose_name='画像データ',  # base64形式の画像データ
        blank=True,
        null=True,
        default='',
    )
    

# Create your models here.
