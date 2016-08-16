# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-14 00:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    #replaces = [(b'moocletpolicy', '0001_initial'), (b'moocletpolicy', '0002_auto_20160607_1242'), (b'moocletpolicy', '0003_auto_20160607_2037'), (b'moocletpolicy', '0004_auto_20160607_2040'), (b'moocletpolicy', '0005_auto_20160617_1314'), (b'moocletpolicy', '0006_auto_20160617_1330'), (b'moocletpolicy', '0007_auto_20160618_1802')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mooclet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SubGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('var1', models.IntegerField()),
                ('var2', models.IntegerField()),
                ('var3', models.IntegerField()),
                ('var4', models.IntegerField()),
                ('var5', models.IntegerField()),
                ('var6', models.IntegerField()),
                ('var7', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SubGroupProbabilityArray',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mooclet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moocletpolicy.Mooclet')),
                ('subgroup', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moocletpolicy.SubGroup')),
            ],
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('mooclet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moocletpolicy.Mooclet')),
            ],
        ),
        migrations.CreateModel(
            name='VersionProbability',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('probability', models.FloatField()),
                ('subgroup_probability_array', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moocletpolicy.SubGroupProbabilityArray')),
                ('version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moocletpolicy.Version')),
            ],
        ),
        migrations.AlterField(
            model_name='subgroup',
            name='var1',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='subgroup',
            name='var2',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='subgroup',
            name='var3',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='subgroup',
            name='var4',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='subgroup',
            name='var5',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='subgroup',
            name='var6',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='subgroup',
            name='var7',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='subgroup',
            name='var1',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='subgroup',
            name='var2',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='subgroup',
            name='var3',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='subgroup',
            name='var4',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='subgroup',
            name='var5',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='subgroup',
            name='var6',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='subgroup',
            name='var7',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='subgroup',
            name='var1',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subgroup',
            name='var2',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subgroup',
            name='var3',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subgroup',
            name='var4',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subgroup',
            name='var5',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subgroup',
            name='var6',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='subgroup',
            name='var7',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('policy_function', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user_id', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='UserVarMoocletVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mooclet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moocletpolicy.Mooclet')),
                ('policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moocletpolicy.Policy')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moocletpolicy.Student')),
            ],
        ),
        migrations.CreateModel(
            name='UserVarNum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('value', models.FloatField(blank=True, null=True)),
                ('descriptor', models.CharField(blank=True, max_length=250, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moocletpolicy.Student')),
            ],
        ),
        migrations.CreateModel(
            name='UserVarText',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('value', models.CharField(blank=True, max_length=2000, null=True)),
                ('descriptor', models.CharField(max_length=250)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moocletpolicy.Student')),
            ],
        ),
        migrations.AddField(
            model_name='version',
            name='text',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name='uservarmoocletversion',
            name='version',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moocletpolicy.Version'),
        ),
        migrations.AlterField(
            model_name='policy',
            name='policy_function',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
