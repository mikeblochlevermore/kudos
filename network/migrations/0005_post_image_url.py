# Generated by Django 4.2.2 on 2023-10-11 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_alter_post_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image_url',
            field=models.CharField(default='https://cdn.theatlantic.com/thumbor/Kto-jp-IrA7TydSu5W5uB1FBDmA=/0x131:2555x1568/1952x1098/media/img/mt/2017/06/shutterstock_319985324/original.jpg', max_length=128),
            preserve_default=False,
        ),
    ]
