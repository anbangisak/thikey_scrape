# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class BaseModelLogger(models.Model):
    """ All model will have created and updated timestamps as logs """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class GovDetail(BaseModelLogger):
    """ Saving the detail page data """

    name = models.TextField(blank=True, null=True)
    img = models.TextField(blank=True, null=True)
    large_img = models.TextField(blank=True, null=True)
    desc = models.TextField(blank=True, null=True)
    upc = models.TextField(blank=True, null=True)
    sku = models.TextField(blank=True, null=True)
    condition = models.TextField(blank=True, null=True)
    category = models.TextField(blank=True, null=True)
    url = models.TextField(blank=True, null=True)
    crawled = models.BooleanField(default=False)

    def __unicode__(self):
        return u"{0} - {1}".format(self.name, self.sku)
