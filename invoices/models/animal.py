from django.db import models


class Animal(models.Model):
    name = models.CharField(max_length=200)
    sound = models.CharField(max_length=200)

    def speak(self):
        return 'The {} says "{}"'.format(self.name, self.sound)
