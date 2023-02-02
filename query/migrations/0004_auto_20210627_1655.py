# Generated by Django 3.2.3 on 2021-06-27 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('query', '0003_auto_20210627_1654'),
    ]

    operations = [
        migrations.CreateModel(
            name='ALabeledimage',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('imageid', models.CharField(db_column='ImageID', max_length=45)),
                ('areaid', models.IntegerField(db_column='AreaID')),
                ('path', models.TextField(blank=True, db_column='Path', null=True)),
                ('pathtype', models.CharField(db_column='PathType', max_length=20)),
                ('userid', models.CharField(db_column='UserID', max_length=45)),
                ('usertype', models.CharField(db_column='UserType', max_length=10)),
                ('userid_check_1', models.CharField(blank=True, db_column='UserID_Check_1', max_length=45, null=True)),
                ('userid_check_2', models.CharField(blank=True, db_column='UserID_Check_2', max_length=45, null=True)),
                ('createdate', models.DateTimeField(blank=True, db_column='CreateDate', null=True)),
                ('patientid', models.CharField(db_column='PatientID', max_length=45)),
            ],
            options={
                'db_table': 'a_labeledimage',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='ALabeledimage2',
        ),
    ]
