# Generated by Django 2.2 on 2019-12-11 07:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_article_posted_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='posted_by',
        ),
        migrations.AddField(
            model_name='article',
            name='editor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='news.Editor'),
            preserve_default=False,
        ),
    ]