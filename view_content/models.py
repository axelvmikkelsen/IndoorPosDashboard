from django.db import models
from django.utils.translation import gettext_lazy
from django.core.validators import MaxValueValidator, MinValueValidator
from django.forms.fields import DateTimeField
from django.utils import timezone

class Room(models.Model):
    roomID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=15)
    x_start = models.PositiveIntegerField()
    x_end = models.PositiveIntegerField()
    y_start = models.PositiveIntegerField()
    y_end = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = gettext_lazy('Rooms')

class Zone(models.Model):
    zoneID = models.AutoField(primary_key=True)
    roomID = models.ForeignKey('Room', on_delete=models.CASCADE)
    name = models.CharField(max_length=15)
    x_start = models.PositiveIntegerField()
    x_end = models.PositiveIntegerField()
    y_start = models.PositiveIntegerField()
    y_end = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = gettext_lazy('Zones')

class Obstruction(models.Model):
    obsID = models.AutoField(primary_key=True)
    roomID = models.ForeignKey('Room', on_delete=models.CASCADE)
    name = models.CharField(max_length=15)
    x_start = models.PositiveIntegerField()
    x_end = models.PositiveIntegerField()
    y_start = models.PositiveIntegerField()
    y_end = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = gettext_lazy('Obstructions')

class Tag(models.Model):
    tagID = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = gettext_lazy('Tags')

class TagLocation(models.Model):
    tagID = models.ForeignKey('Tag',on_delete=models.CASCADE, null=False)
    timestamp = models.FloatField(default=0)
    x_pos = models.FloatField(default=0)
    y_pos = models.FloatField(default=0)
    vx = models.FloatField(default=0)
    vy = models.FloatField(default=0)

    def __str__(self):
        return "TagLocation"

    class Meta:
        verbose_name_plural = gettext_lazy('taglocation')

class Connection(models.Model):
    connID = models.AutoField(primary_key=True)
    connected = models.BooleanField(default=False)
    host = models.CharField(max_length=50)
    port = models.PositiveIntegerField()
    topic = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    sampling = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.host

    class Meta:
        verbose_name_plural = gettext_lazy('Connection')

class Session(models.Model):
    sessionID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=15)
    duration = models.PositiveIntegerField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = gettext_lazy('Sessions')
