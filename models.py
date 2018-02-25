from django.db import models

# Create your models here.

class Visitor(models.Model):
    """
    Users

    """
    ip = models.CharField(max_length=150, null=True, blank=True)
    class Meta:
        verbose_name_plural = 'Visitors'
        ordering = ['ip']

    def __str__(self):
        return str(self.ip)


class Record_Visitor(models.Model):
    """
    Records the Traffic Of Users

    """
    ip = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    total_today = models.BigIntegerField(null=True, blank=True)
    total_overall = models.BigIntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Record_Visitors'
        ordering = ['date']

    def __str__(self):
        return str(self.ip)


class Counter(models.Model):
    """
    Records the Traffic Of Users

    """
    date = models.DateField(null=True, blank=True)
    total_today = models.BigIntegerField(null=True, blank=True)
    total_overall = models.BigIntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Counters'
        ordering = ['date']

    def __str__(self):
        return str(self.date)