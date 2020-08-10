# Generated by Django 2.2.3 on 2019-08-06 04:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contentType', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('contentId', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Common',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contentId', models.IntegerField(unique=True)),
                ('sigungu', models.IntegerField(null=True)),
                ('area', models.IntegerField(null=True)),
                ('mapx', models.FloatField(null=True)),
                ('mapy', models.FloatField(null=True)),
                ('category', models.IntegerField(null=True)),
                ('title', models.TextField(null=True)),
                ('tel', models.TextField(null=True)),
                ('overview', models.TextField(null=True)),
                ('addr1', models.TextField(null=True)),
                ('addr2', models.TextField(null=True)),
                ('homepage', models.TextField(null=True)),
                ('avgScore', models.FloatField(null=True)),
                ('zipCode', models.TextField(null=True)),
                ('image', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detailId', models.IntegerField()),
                ('startTime', models.TextField(null=True)),
                ('endTime', models.TextField(null=True)),
                ('parking', models.TextField(null=True)),
                ('chkPet', models.TextField(null=True)),
                ('chkBaby', models.TextField(null=True)),
                ('restDate', models.TextField(null=True)),
                ('useTime', models.TextField(null=True)),
                ('ageLimit', models.TextField(null=True)),
                ('pay', models.TextField(null=True)),
                ('barbeque', models.TextField(null=True)),
                ('refund', models.TextField(null=True)),
                ('subevent', models.TextField(null=True)),
                ('openPeriod', models.TextField(null=True)),
                ('discountInfo', models.TextField(null=True)),
                ('chkCook', models.TextField(null=True)),
                ('openTime', models.TextField(null=True)),
                ('chkPack', models.TextField(null=True)),
                ('chkSmoking', models.TextField(null=True)),
                ('infoCenter', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)], null=True)),
                ('content', models.TextField(default='', null=True)),
                ('contentId', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Stamp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('inform', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='maps.Common')),
            ],
        ),
    ]