from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta

PRINCIPLES = (
    (1, 'Authority'),
    (2, 'Complementarity'),
    (3, 'Privacy'),
    (4, 'Attribution'),
    (5, 'Justification'),
    (6, 'Transparency'),
    (7, 'Financial Disclosure'),
    (8, 'Advertising Policy'),
    )

class Category(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True)
    name = models.CharField(max_length=86)
    slug = models.SlugField(max_length=86)
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'

class Cert(models.Model):
    # Primary key ID field is created automatically
    owner  = models.ForeignKey(User, related_name='owner', help_text="User who submited certification request.")
    editor = models.ForeignKey(User, related_name='editor', verbose_name="HON editor", default=1,
        limit_choices_to = {'is_staff': True})
    name = models.CharField(max_length=86, verbose_name="Website name")
    link = models.URLField()
    compliant = models.BooleanField(help_text='Is in compliance with the HONcode?')
    date_valid_from  = models.DateField('Valid from', default=datetime.now)
    date_valid_until = models.DateField('Valid until', blank=True,
        help_text="Fill-in if different from standard 1 year after initial validation.")
    date_init_review = models.DateField('Initial review', default=datetime.now)
    date_last_visit  = models.DateField('Last visit', default=datetime.now)
    
    category1 = models.ForeignKey(Category, related_name='category1', blank=True, null=True)
    category2 = models.ForeignKey(Category, related_name='category2', blank=True, null=True)
    category3 = models.ForeignKey(Category, related_name='category3', blank=True, null=True)
    
    def pin(self):
        return 'HONConduct%d' % self.pk
    
    def domain(self):
        return self.link.split('//')[1].split('/')[0]
    
    def __unicode__(self):
        return self.pin()
    
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('hon.cert.views.cert', args=[str(self.pk)])
    
    def save(self, *args, **kwargs):
        # set the expiration automatically
        if not self.date_valid_until:
            self.date_valid_until = self.date_valid_from + timedelta(days=365)
        super(Cert, self).save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'certificate'
    
class Proof(models.Model):
    cert = models.ForeignKey(Cert)
    princip = models.IntegerField(choices=PRINCIPLES, verbose_name="Principle")
    desc = models.CharField(max_length=512, verbose_name='Description')
    date = models.DateField(default=datetime.now)
    link = models.URLField(blank=True, help_text="Fill-in if different from certified website link.")
    
    def __unicode__(self):
        return self.get_princip_display()
    
    def save(self, *args, **kwargs):
        # inherit link to homepage from parent certificate if link isn't provided
        if not self.link:
            self.link = self.cert.link
        super(Proof, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['princip']