
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('ocr', '0003_ocrresult_email_ocrresult_name_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ocrresult',
            old_name='email',
            new_name='gmail',
        ),
        migrations.RemoveField(
            model_name='ocrresult',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='ocrresult',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='ocrresult',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
