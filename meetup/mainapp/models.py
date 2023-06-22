from django.db import models
from django.core import validators


class Event(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    event_name = models.CharField(max_length=50)
    place = models.CharField(max_length=50)
    is_over = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.event_name} {self.date}'


class Speaker(models.Model):
    tg_id = models.CharField(max_length=30, unique=True)
    full_name = models.CharField(max_length=50)
    workplace = models.CharField(max_length=50)
    experience = models.TextField()
    events = models.ManyToManyField(Event)

    def __str__(self) -> str:
        return f'{self.full_name}'


class Report(models.Model):
    report_title = models.CharField(max_length=50)
    planed_start_time = models.TimeField()
    planed_end_time = models.TimeField()
    actual_start_time = models.TimeField(null=True)
    actual_end_time = models.TimeField(null=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    speaker = models.OneToOneField(Speaker, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.report_title}'

    def is_report_over(self):
        if self.actual_end_time:
            return True
        return False


class User(models.Model):
    email = models.EmailField(
        max_length=254, null=True,
        validators=[validators.EmailValidator(message="Invalid Email")])
    tg_id = models.CharField(max_length=30, unique=True)

    def __str__(self) -> str:
        return f"User's telegram id: {self.tg_id}"


class Question(models.Model):
    question_text = models.TextField(unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    speaker = models.OneToOneField(Speaker, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.question_text}'
