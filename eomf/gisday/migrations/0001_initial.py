# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUsGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=125)),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='AboutUsPerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=100, null=True, blank=True)),
                ('middle_name', models.CharField(max_length=50, null=True, blank=True)),
                ('last_name', models.CharField(max_length=100, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('phone', models.CharField(max_length=16, null=True, blank=True)),
                ('headshot', models.ImageField(default=b'gisday/aboutus/dummy_headshot222.jpg', null=True, upload_to=b'gisday/aboutus/')),
            ],
        ),
        migrations.CreateModel(
            name='Agenda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('entry_name', models.CharField(max_length=100, null=True, blank=True)),
                ('time_ini', models.TimeField()),
                ('time_end', models.TimeField(null=True, blank=True)),
                ('speaker', models.CharField(max_length=160, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.PositiveIntegerField()),
                ('entry_name', models.CharField(max_length=100, null=True, blank=True)),
                ('content', tinymce.models.HTMLField(null=True, blank=True)),
                ('date', models.DateField(null=True, blank=True)),
                ('image', models.ImageField(null=True, upload_to=b'gisday/announcements/', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Booth',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('non_profit', models.BooleanField()),
                ('institution', models.CharField(max_length=128)),
                ('department', models.CharField(max_length=128)),
                ('last_name', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=50)),
                ('address_1', models.CharField(max_length=128)),
                ('address_2', models.CharField(max_length=128, null=True, blank=True)),
                ('city', models.CharField(max_length=30)),
                ('state', models.CharField(max_length=30)),
                ('zipcode', models.CharField(max_length=30)),
                ('phone', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=60)),
                ('names', models.TextField(null=True, verbose_name=b'Aditional atendees', blank=True)),
                ('permits', models.CharField(max_length=128, null=True, verbose_name=b'No. of parking permits needed', blank=True)),
                ('oversized', models.NullBooleanField()),
                ('comment', models.TextField(null=True, verbose_name=b'Questions & comments', blank=True)),
                ('tshirt_size_1', models.CharField(max_length=3, choices=[(b'UK', b'Unkown'), (b'S', b'Small'), (b'M', b'Medium'), (b'L', b'Large'), (b'XL', b'Extra Large'), (b'2XL', b'Extra Extra Large')])),
                ('tshirt_size_2', models.CharField(max_length=3, choices=[(b'UK', b'Unkown'), (b'S', b'Small'), (b'M', b'Medium'), (b'L', b'Large'), (b'XL', b'Extra Large'), (b'2XL', b'Extra Extra Large')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('validated', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='BoothContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', tinymce.models.HTMLField(null=True, blank=True)),
                ('max_booths', models.PositiveIntegerField(default=30)),
                ('registration_message_non_profit', tinymce.models.HTMLField(null=True, blank=True)),
                ('registration_message_profit', tinymce.models.HTMLField(null=True, blank=True)),
                ('registration_recipients', models.CharField(default=b'gisday@ou.edu', max_length='600')),
            ],
        ),
        migrations.CreateModel(
            name='CommitteeContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', tinymce.models.HTMLField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='DemographicSurvey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('institution', models.CharField(max_length=80, verbose_name=b'Participant Institution', choices=[(b'Oklahoma State University', b'Oklahoma State University'), (b'Samuel Roberts Noble Foundation', b'Samuel Roberts Noble Foundation'), (b'University of Oklahoma', b'University of Oklahoma'), (b'University of Tulsa', b'University of Tulsa'), (b'Other', b'Other please specify')])),
                ('other_institution', models.CharField(max_length=80, null=True, verbose_name=b'If other, please specify', blank=True)),
                ('position', models.CharField(max_length=80, verbose_name=b'Participant Position', choices=[(b'Community College Faculty', b'Community College Faculty'), (b'Doctoral Student', b'Doctoral Student'), (b'EPSCoR Staff', b'EPSCoR Staff'), (b'Government Staff', b'Government Staff'), (b'Graduate Faculty', b'Graduate Faculty'), (b'Higher Education Faculty', b'Higher Education Faculty'), (b'K-12 Administrator', b'K-12 Administrator'), (b'K-12 Teacher', b'K-12 Teacher'), (b'K-12 Student', b'K-12 Student'), (b"Master's Student", b"Master's Student"), (b'Other Pre-College Teachers', b'Other Pre-College Teachers'), (b'Post-Doctoral Researcher', b'Post-Doctoral Researcher'), (b'Researcher', b'Researcher'), (b'REU Participant', b'REU Participant'), (b'Technical School Faculty', b'Technical School Faculty'), (b'Technical School Student', b'Technical School Student'), (b'Staff - Technical', b'Staff - Technical'), (b'Staff - Non-Technical', b'Staff - Non-Technical'), (b'Undergraduate Faculty', b'Undergraduate Faculty'), (b'Undergraduate Student', b'Undergraduate Student'), (b'Other', b'Other please specify')])),
                ('other_position', models.CharField(max_length=80, null=True, verbose_name=b'If other, please specify', blank=True)),
                ('highest_degree', models.CharField(max_length=20, verbose_name=b'Highest Degree Obtained', choices=[(b'High School', b'High School'), (b'Associate', b'Associate'), (b"Bachelor's", b"Bachelor's"), (b"Master's", b"Master's"), (b'Doctoral', b'Doctoral')])),
                ('gender', models.CharField(max_length=20, verbose_name=b'Gender', choices=[(b'Female', b'Female'), (b'Male', b'Male'), (b'NR', b'Prefer not to respond')])),
                ('ethnicity', models.CharField(max_length=20, verbose_name=b'Ethnicity', choices=[(b'Hispanic/Latino', b'Hispanic/Latino'), (b'Not Hispanic/Latino', b'Not Hispanic/Latino'), (b'NR', b'Prefer not to respond')])),
                ('citizenship', models.CharField(max_length=30, verbose_name=b'Citizenship', choices=[(b'US Citizen', b'US Citizen'), (b'Permanent Resident', b'Permanent Resident'), (b'Non-Us Citizen', b'Non-Us Citizen'), (b'NR', b'Prefer not to respond')])),
                ('race', models.CharField(max_length=50, verbose_name=b'Race', choices=[(b'American Indian or Alaskan Native', b'American Indian or Alaskan Native'), (b'Asian', b'Asian'), (b'Black or African American ', b'Black or African American '), (b'Native Hawaiian or Pacific Islander', b'Native Hawaiian or Pacific Islander'), (b'White', b'White'), (b'Prefer not to respond', b'Prefer not to respond'), (b'Other', b'Other (please specify)')])),
                ('other_race', models.CharField(max_length=50, null=True, verbose_name=b'If other, please specify', blank=True)),
                ('disability', models.CharField(max_length=50, verbose_name=b'Disability', choices=[(b'Hearing Impairment', b'Hearing Impairment'), (b'Mobility/Orthopedic impairment', b'Mobility/Orthopedic impairment'), (b'Visual Impairment', b'Visual Impairment'), (b'None', b'None'), (b'Prefer not to respond', b'Prefer not to respond'), (b'Other', b'Other (please specify)')])),
                ('other_disability', models.CharField(max_length=50, null=True, verbose_name=b'If other, please specify', blank=True)),
                ('parents_degree', models.CharField(max_length=80, verbose_name=b'In your family, which of your parents/guardians received college degrees?', choices=[(b'Neither', b'Neither my mother or father (neither of my guardians)'), (b'Both', b'Both my mother and father (both my guardians)'), (b'Father', b'Only my father (male guardian)'), (b'Mother', b'Only my mother (female guardian)'), (b"Don't know", b'I do not know'), (b'NR', b'Prefer not to respond')])),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='GisDayPhoto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('picture', models.ImageField(null=True, upload_to=b'gisday/gallery/')),
            ],
        ),
        migrations.CreateModel(
            name='ItemDonor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=160, null=True, blank=True)),
                ('link', models.CharField(max_length=300, null=True, blank=True)),
                ('logo', models.ImageField(null=True, upload_to=b'gisday/item_donors/')),
            ],
        ),
        migrations.CreateModel(
            name='ItemInYear',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=160, null=True, blank=True)),
                ('value', models.DecimalField(max_digits=10, decimal_places=2)),
                ('link', models.CharField(max_length=160, null=True, blank=True)),
                ('donor', models.ForeignKey(to='gisday.ItemDonor', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='LogisticsContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', tinymce.models.HTMLField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='OverviewContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', tinymce.models.HTMLField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='OverviewImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'gisday/overview/')),
                ('order', models.IntegerField()),
                ('title', models.CharField(max_length=300, null=True, blank=True)),
                ('description', models.CharField(max_length=300, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PersonInGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('highlight', models.BooleanField(default=False)),
                ('group', models.ForeignKey(related_name='pvsgInGroup', to='gisday.AboutUsGroup', on_delete=models.CASCADE)),
                ('person', models.ForeignKey(related_name='pvsgInPerson', to='gisday.AboutUsPerson', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='PhotoContestContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', tinymce.models.HTMLField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PhotoContestParticipant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_name', models.CharField(max_length=50, verbose_name=b'Last name')),
                ('first_name', models.CharField(max_length=50, verbose_name=b'First name')),
                ('email', models.EmailField(max_length=60, verbose_name=b'email')),
                ('comment', models.TextField(null=True, verbose_name=b'Questions & comments', blank=True)),
                ('validated', models.BooleanField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='Poster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_name', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('institution', models.CharField(max_length=128)),
                ('department', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=30)),
                ('title', models.CharField(max_length=200)),
                ('authors', models.TextField(null=True, verbose_name=b'Poster author list', blank=True)),
                ('abstract', models.TextField(verbose_name=b'Poster abstract')),
                ('comment', models.TextField(null=True, verbose_name=b'Questions & comments', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('validated', models.BooleanField()),
                ('preview', models.FileField(max_length=300, null=True, upload_to=b'gisday/posters/', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PosterCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='PosterContestContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', tinymce.models.HTMLField(null=True, blank=True)),
                ('registration_message', tinymce.models.HTMLField(null=True, blank=True)),
                ('registration_recipients', models.CharField(default=b'gisday@ou.edu', max_length='600')),
            ],
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=160, null=True, blank=True)),
                ('contact_person_name', models.CharField(max_length=160, null=True, blank=True)),
                ('contact_person_phone', models.CharField(max_length=15, null=True, blank=True)),
                ('contact_person_mail', models.CharField(max_length=160, null=True, blank=True)),
                ('link', models.CharField(max_length=300, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SponsorCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('min_inversion', models.IntegerField()),
                ('max_inversion', models.IntegerField()),
                ('logo', models.ImageField(null=True, upload_to=b'gisday/sponsors/')),
            ],
        ),
        migrations.CreateModel(
            name='SponsorInYear',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('money', models.IntegerField()),
                ('category', models.ForeignKey(related_name='categoryOfSponsorInYear', to='gisday.SponsorCategory', on_delete=models.CASCADE)),
                ('sponsor', models.ForeignKey(to='gisday.Sponsor', on_delete=models.CASCADE)),
            ],
        ),
        migrations.CreateModel(
            name='SponsorsContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', tinymce.models.HTMLField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SummaryContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', tinymce.models.HTMLField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='SurveyContents',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', tinymce.models.HTMLField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_name', models.CharField(max_length=100)),
                ('first_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=30)),
                ('institution', models.CharField(max_length=100)),
                ('comment', models.TextField(null=True, verbose_name=b'Questions & comments', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('validated', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='VisitorRegistrationContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', tinymce.models.HTMLField(null=True, blank=True)),
                ('registration_message', tinymce.models.HTMLField(null=True, blank=True)),
                ('registration_recipients', models.CharField(default=b'gisday@ou.edu', max_length='600')),
            ],
        ),
        migrations.CreateModel(
            name='Year',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('registration_closed', models.BooleanField(default=False)),
                ('address', models.CharField(max_length=300, null=True, blank=True)),
                ('hidden', models.BooleanField(default=False)),
                ('time_ini', models.TimeField()),
                ('time_end', models.TimeField()),
                ('summary_hidden', models.BooleanField(default=True)),
                ('agenda_hidden', models.BooleanField(default=True)),
                ('photo_contest_hidden', models.BooleanField(default=True)),
                ('poster_contest_hidden', models.BooleanField(default=True)),
                ('image_gallery_hidden', models.BooleanField(default=True)),
                ('photo_gallery_hidden', models.BooleanField(default=True)),
                ('facebook_link', models.CharField(max_length=300, null=True, blank=True)),
                ('twitter_link', models.CharField(max_length=300, null=True, blank=True)),
                ('survey_open', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('demographicsurvey_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='gisday.DemographicSurvey', on_delete=models.CASCADE)),
                ('participate_again', models.BooleanField(verbose_name=b'I would like to participate in the event again')),
                ('role', models.CharField(max_length=50, verbose_name=b'What was you primary role in the event?', choices=[(b'Organizing Committee', b'Organizing Committee'), (b'Faculty Poster Judge', b'Faculty Poster Judge'), (b'Student Poster Contestant', b'Student Poster Contestant'), (b'Booth Exhibitor', b'Booth Exhibitor'), (b'Poster Exhibitor', b'Poster Exhibitor'), (b'Student Facilitator/Volunteer', b'Student Facilitator/Volunteer'), (b'Staff Facilitator', b'Staff Facilitator'), (b'Other', b'Other (please specify)')])),
                ('other_role', models.CharField(max_length=80, null=True, verbose_name=b'If other, please specify', blank=True)),
                ('beneficial_aspects', models.TextField(verbose_name=b'What was the most beneficial or interesting aspect of the event?')),
                ('comments_and_suggestions', models.TextField(null=True, verbose_name=b'Please provide any additional comments or suggestions:', blank=True)),
            ],
            bases=('gisday.demographicsurvey',),
        ),
        migrations.AddField(
            model_name='visitorregistrationcontent',
            name='year',
            field=models.ForeignKey(to='gisday.Year', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='visitor',
            name='year',
            field=models.ForeignKey(to='gisday.Year', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='surveycontents',
            name='year',
            field=models.ForeignKey(to='gisday.Year', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='summarycontent',
            name='year',
            field=models.ForeignKey(to='gisday.Year', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='sponsorscontent',
            name='year',
            field=models.ForeignKey(to='gisday.Year', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='sponsorinyear',
            name='year',
            field=models.ForeignKey(to='gisday.Year', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='postercontestcontent',
            name='year',
            field=models.ForeignKey(to='gisday.Year', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='poster',
            name='category',
            field=models.ForeignKey(to='gisday.PosterCategory', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='poster',
            name='year',
            field=models.ForeignKey(to='gisday.Year', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='photocontestparticipant',
            name='year',
            field=models.ForeignKey(to='gisday.Year', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='photocontestcontent',
            name='year',
            field=models.ForeignKey(to='gisday.Year', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='personingroup',
            name='year',
            field=models.ForeignKey(to='gisday.Year', on_delete=models.CASCADE),
        ),
        migrations.AlterUniqueTogether(
            name='overviewimage',
            unique_together=set([('order',)]),
        ),
        migrations.AddField(
            model_name='logisticscontent',
            name='year',
            field=models.ForeignKey(to='gisday.Year', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='iteminyear',
            name='year',
            field=models.ForeignKey(to='gisday.Year', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='gisdayphoto',
            name='year',
            field=models.ForeignKey(to='gisday.Year', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='demographicsurvey',
            name='year',
            field=models.ForeignKey(to='gisday.Year', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='committeecontent',
            name='year',
            field=models.ForeignKey(to='gisday.Year', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='boothcontent',
            name='year',
            field=models.ForeignKey(to='gisday.Year', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='booth',
            name='year',
            field=models.ForeignKey(to='gisday.Year', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='announcement',
            name='year',
            field=models.ForeignKey(to='gisday.Year', on_delete=models.CASCADE),
        ),
        migrations.AddField(
            model_name='agenda',
            name='year',
            field=models.ForeignKey(to='gisday.Year', on_delete=models.CASCADE),
        ),
        migrations.AlterUniqueTogether(
            name='visitorregistrationcontent',
            unique_together=set([('year',)]),
        ),
        migrations.AlterUniqueTogether(
            name='visitor',
            unique_together=set([('year', 'email')]),
        ),
        migrations.AlterUniqueTogether(
            name='surveycontents',
            unique_together=set([('year',)]),
        ),
        migrations.AlterUniqueTogether(
            name='summarycontent',
            unique_together=set([('year',)]),
        ),
        migrations.AlterUniqueTogether(
            name='sponsorscontent',
            unique_together=set([('year',)]),
        ),
        migrations.AlterUniqueTogether(
            name='sponsorinyear',
            unique_together=set([('sponsor', 'year')]),
        ),
        migrations.AlterUniqueTogether(
            name='postercontestcontent',
            unique_together=set([('year',)]),
        ),
        migrations.AlterUniqueTogether(
            name='poster',
            unique_together=set([('year', 'email')]),
        ),
        migrations.AlterUniqueTogether(
            name='photocontestcontent',
            unique_together=set([('year',)]),
        ),
        migrations.AlterUniqueTogether(
            name='logisticscontent',
            unique_together=set([('year',)]),
        ),
        migrations.AlterUniqueTogether(
            name='committeecontent',
            unique_together=set([('year',)]),
        ),
        migrations.AlterUniqueTogether(
            name='boothcontent',
            unique_together=set([('year',)]),
        ),
        migrations.AlterUniqueTogether(
            name='booth',
            unique_together=set([('year', 'institution', 'department')]),
        ),
        migrations.AlterUniqueTogether(
            name='announcement',
            unique_together=set([('year', 'position')]),
        ),
        migrations.AlterUniqueTogether(
            name='agenda',
            unique_together=set([('year', 'entry_name')]),
        ),
    ]
