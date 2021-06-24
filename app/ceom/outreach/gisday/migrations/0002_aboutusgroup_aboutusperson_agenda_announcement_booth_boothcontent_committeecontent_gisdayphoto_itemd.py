# Generated by Django 3.2.4 on 2021-06-20 23:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('gisday', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUsGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=125)),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='AboutUsPerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=16, null=True)),
                ('headshot', models.ImageField(default='gisday/aboutus/dummy_headshot222.jpg', null=True, upload_to='gisday/aboutus/')),
            ],
        ),
        migrations.CreateModel(
            name='ItemDonor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=160, null=True)),
                ('link', models.CharField(blank=True, max_length=300, null=True)),
                ('logo', models.ImageField(null=True, upload_to='gisday/item_donors/')),
            ],
        ),
        migrations.CreateModel(
            name='PosterCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=160, null=True)),
                ('contact_person_name', models.CharField(blank=True, max_length=160, null=True)),
                ('contact_person_phone', models.CharField(blank=True, max_length=15, null=True)),
                ('contact_person_mail', models.CharField(blank=True, max_length=160, null=True)),
                ('link', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SponsorCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('min_inversion', models.IntegerField()),
                ('max_inversion', models.IntegerField()),
                ('logo', models.ImageField(null=True, upload_to='gisday/sponsors/')),
            ],
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('registration_closed', models.BooleanField(default=False)),
                ('address', models.CharField(blank=True, max_length=300, null=True)),
                ('hidden', models.BooleanField(default=False)),
                ('time_ini', models.TimeField()),
                ('time_end', models.TimeField()),
                ('summary_hidden', models.BooleanField(default=True)),
                ('agenda_hidden', models.BooleanField(default=True)),
                ('photo_contest_hidden', models.BooleanField(default=True)),
                ('poster_contest_hidden', models.BooleanField(default=True)),
                ('image_gallery_hidden', models.BooleanField(default=True)),
                ('photo_gallery_hidden', models.BooleanField(default=True)),
                ('facebook_link', models.CharField(blank=True, max_length=300, null=True)),
                ('twitter_link', models.CharField(blank=True, max_length=300, null=True)),
                ('survey_open', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=100, null=True)),
                ('first_name', models.CharField(max_length=100, null=True)),
                ('prole', models.CharField(max_length=20, null=True)),
                ('lunch', models.CharField(max_length=4)),
                ('TShirtSize', models.CharField(max_length=20, null=True)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisday.year')),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution', models.CharField(max_length=80, verbose_name='Participant Institution')),
                ('other_institution', models.CharField(blank=True, max_length=80, null=True, verbose_name='If other, please specify')),
                ('position', models.CharField(max_length=80, verbose_name='Participant Position')),
                ('other_position', models.CharField(blank=True, max_length=80, null=True, verbose_name='If other, please specify')),
                ('highest_degree', models.CharField(max_length=20, null=True, verbose_name='Highest Degree Obtained')),
                ('gender', models.CharField(max_length=50, verbose_name='Gender')),
                ('ethnicity', models.CharField(max_length=50, verbose_name='Ethnicity')),
                ('citizenship', models.CharField(max_length=50, verbose_name='Citizenship')),
                ('race', models.CharField(max_length=50, verbose_name='Race')),
                ('other_race', models.CharField(blank=True, max_length=50, null=True, verbose_name='If other, please specify')),
                ('disability', models.CharField(max_length=50, verbose_name='Disability')),
                ('other_disability', models.CharField(blank=True, max_length=50, null=True, verbose_name='If other, please specify')),
                ('parents_degree', models.CharField(max_length=80, null=True, verbose_name='In your family, which of your parents/guardians received college degrees?')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('participate_again', models.BooleanField(verbose_name='I would like to participate in the event again')),
                ('role', models.CharField(choices=[('Organizing Committee', 'Organizing Committee'), ('Faculty Poster Judge', 'Faculty Poster Judge'), ('Student Poster Contestant', 'Student Poster Contestant'), ('Booth Exhibitor', 'Booth Exhibitor'), ('Poster Exhibitor', 'Poster Exhibitor'), ('Student Facilitator/Volunteer', 'Student Facilitator/Volunteer'), ('Staff Facilitator', 'Staff Facilitator'), ('Other', 'Other (please specify)')], max_length=50, verbose_name='What was you primary role in the event?')),
                ('other_role', models.CharField(blank=True, max_length=80, null=True, verbose_name='If other, please specify')),
                ('beneficial_aspects', models.TextField(verbose_name='What was the most beneficial or interesting aspect of the event?')),
                ('comments_and_suggestions', models.TextField(blank=True, null=True, verbose_name='Please provide any additional comments or suggestions:')),
                ('year', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gisday.year')),
            ],
        ),
        migrations.CreateModel(
            name='PhotoContestParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last name')),
                ('first_name', models.CharField(max_length=50, verbose_name='First name')),
                ('email', models.EmailField(max_length=60, verbose_name='email')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Questions & comments')),
                ('validated', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisday.year')),
            ],
        ),
        migrations.CreateModel(
            name='PersonInGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('highlight', models.BooleanField(default=False)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pvsgInGroup', to='gisday.aboutusgroup')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pvsgInPerson', to='gisday.aboutusperson')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisday.year')),
            ],
        ),
        migrations.CreateModel(
            name='ItemInYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=160, null=True)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('link', models.CharField(blank=True, max_length=160, null=True)),
                ('donor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisday.itemdonor')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisday.year')),
            ],
        ),
        migrations.CreateModel(
            name='GisDayPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(null=True, upload_to='gisday/gallery/')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisday.year')),
            ],
        ),
        migrations.CreateModel(
            name='VisitorRegistrationContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', tinymce.models.HTMLField(blank=True, null=True)),
                ('registration_message', tinymce.models.HTMLField(blank=True, null=True)),
                ('registration_recipients', models.CharField(default='gisday@ou.edu', max_length=600)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisday.year')),
            ],
            options={
                'unique_together': {('year',)},
            },
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=30)),
                ('institution', models.CharField(max_length=100)),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Questions & comments')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('validated', models.BooleanField()),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisday.year')),
            ],
            options={
                'unique_together': {('year', 'email')},
            },
        ),
        migrations.CreateModel(
            name='SurveyContents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', tinymce.models.HTMLField(blank=True, null=True)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisday.year')),
            ],
            options={
                'unique_together': {('year',)},
            },
        ),
        migrations.CreateModel(
            name='SummaryContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', tinymce.models.HTMLField(blank=True, null=True)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisday.year')),
            ],
            options={
                'unique_together': {('year',)},
            },
        ),
        migrations.CreateModel(
            name='SponsorsContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', tinymce.models.HTMLField(blank=True, null=True)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisday.year')),
            ],
            options={
                'unique_together': {('year',)},
            },
        ),
        migrations.CreateModel(
            name='SponsorInYear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money', models.IntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categoryOfSponsorInYear', to='gisday.sponsorcategory')),
                ('sponsor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisday.sponsor')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisday.year')),
            ],
            options={
                'unique_together': {('sponsor', 'year')},
            },
        ),
        migrations.CreateModel(
            name='PosterContestContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', tinymce.models.HTMLField(blank=True, null=True)),
                ('registration_message', tinymce.models.HTMLField(blank=True, null=True)),
                ('registration_recipients', models.CharField(default='gisday@ou.edu', max_length=600)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisday.year')),
            ],
            options={
                'unique_together': {('year',)},
            },
        ),
        migrations.CreateModel(
            name='Poster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('institution', models.CharField(max_length=128)),
                ('department', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=30)),
                ('title', models.CharField(max_length=200)),
                ('authors', models.TextField(blank=True, null=True, verbose_name='Poster author list')),
                ('abstract', models.TextField(verbose_name='Poster abstract')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Questions & comments')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('validated', models.BooleanField()),
                ('preview', models.FileField(blank=True, max_length=300, null=True, upload_to='gisday/posters/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisday.postercategory')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisday.year')),
            ],
            options={
                'unique_together': {('year', 'email')},
            },
        ),
        migrations.CreateModel(
            name='PhotoContestContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', tinymce.models.HTMLField(blank=True, null=True)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisday.year')),
            ],
            options={
                'unique_together': {('year',)},
            },
        ),
        migrations.CreateModel(
            name='LogisticsContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', tinymce.models.HTMLField(blank=True, null=True)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisday.year')),
            ],
            options={
                'unique_together': {('year',)},
            },
        ),
        migrations.CreateModel(
            name='CommitteeContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', tinymce.models.HTMLField(blank=True, null=True)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisday.year')),
            ],
            options={
                'unique_together': {('year',)},
            },
        ),
        migrations.CreateModel(
            name='BoothContent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', tinymce.models.HTMLField(blank=True, null=True)),
                ('max_booths', models.PositiveIntegerField(default=30)),
                ('registration_message_non_profit', tinymce.models.HTMLField(blank=True, null=True)),
                ('registration_message_profit', tinymce.models.HTMLField(blank=True, null=True)),
                ('registration_recipients', models.CharField(default='gisday@ou.edu', max_length=600)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisday.year')),
            ],
            options={
                'unique_together': {('year',)},
            },
        ),
        migrations.CreateModel(
            name='Booth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('non_profit', models.BooleanField()),
                ('institution', models.CharField(max_length=128)),
                ('department', models.CharField(max_length=128)),
                ('last_name', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('address_1', models.CharField(max_length=128)),
                ('address_2', models.CharField(blank=True, max_length=128, null=True)),
                ('city', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=30)),
                ('zipcode', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=60)),
                ('names', models.TextField(blank=True, null=True, verbose_name='Aditional atendees')),
                ('permits', models.CharField(blank=True, max_length=128, null=True, verbose_name='No. of parking permits needed')),
                ('oversized', models.BooleanField(blank=True, null=True, verbose_name='Do you have a oversized exhibit or display?')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='Questions & comments')),
                ('tshirt_size_1', models.CharField(choices=[('UK', 'Unkown'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large'), ('2XL', 'Extra Extra Large')], max_length=3)),
                ('tshirt_size_2', models.CharField(choices=[('UK', 'Unkown'), ('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large'), ('2XL', 'Extra Extra Large')], max_length=3)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('validated', models.BooleanField()),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisday.year')),
            ],
            options={
                'unique_together': {('year', 'institution', 'department')},
            },
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField()),
                ('entry_name', models.CharField(blank=True, max_length=100, null=True)),
                ('content', tinymce.models.HTMLField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='gisday/announcements/')),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisday.year')),
            ],
            options={
                'unique_together': {('year', 'position')},
            },
        ),
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_name', models.CharField(blank=True, max_length=100, null=True)),
                ('time_ini', models.TimeField()),
                ('time_end', models.TimeField(blank=True, null=True)),
                ('speaker', models.CharField(blank=True, max_length=160, null=True)),
                ('year', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gisday.year')),
            ],
            options={
                'unique_together': {('year', 'entry_name')},
            },
        ),
    ]
