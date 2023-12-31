# Generated by Django 4.2 on 2023-07-02 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=220)),
                ('description', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('video_id', models.CharField(max_length=30, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('state', models.CharField(choices=[('PU', 'Publish'), ('DR', 'Draft')], default='DR', max_length=2)),
                ('publish_time_stamp', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VideoAllProxy',
            fields=[
            ],
            options={
                'verbose_name': 'All Videos',
                'verbose_name_plural': 'All Videos',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('videos.video',),
        ),
        migrations.CreateModel(
            name='VideoProxy',
            fields=[
            ],
            options={
                'verbose_name': 'Published Videos',
                'verbose_name_plural': 'Published Videos',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('videos.video',),
        ),
    ]
