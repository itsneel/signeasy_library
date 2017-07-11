# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sku', models.CharField(unique=True, max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('description', models.BooleanField(default=True)),
                ('total', models.IntegerField(default=0)),
                ('extra_info', jsonfield.fields.JSONField(default={})),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='BookIssue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(related_name='issued', to='books.Book')),
                ('member', models.ForeignKey(related_name='issued_books', to='members.Member')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='book',
            unique_together=set([('sku', 'name')]),
        ),
        migrations.AlterIndexTogether(
            name='book',
            index_together=set([('sku', 'name')]),
        ),
        migrations.AlterIndexTogether(
            name='bookissue',
            index_together=set([('member', 'book')]),
        ),
    ]
