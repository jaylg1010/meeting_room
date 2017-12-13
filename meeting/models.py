from django.db import models

# Create your models here.

class UserInfo(models.Model):
    username=models.CharField(max_length=32,verbose_name="用户名")
    password=models.CharField(max_length=64,verbose_name="密码")

    def __str__(self):
        return self.username


class MeetingRoom(models.Model):
    title=models.CharField(max_length=32,verbose_name="会议室名称")

    def __str__(self):
        return self.title

class Booking(models.Model):
    user=models.ForeignKey(to=UserInfo,verbose_name="预定会议室的用户")
    room=models.ForeignKey(to=MeetingRoom,verbose_name="预定的会议室")

    booking_date=models.DateField(verbose_name="预定的日期")

    time_choices = (
        (1,"8:00"),
        (2,"9:00"),
        (3,"10:00"),
        (4, '11:00'),
        (5, '12:00'),
        (6, '13:00'),
        (7, '14:00'),
        (8, '15:00'),
        (9, '16:00'),
        (10, '17:00'),
        (11, '18:00'),
        (12, '19:00'),
        (13, '20:00'),
    )

    booking_time=models.IntegerField(choices=time_choices,verbose_name='预定的时间段')

    class Meta:
        unique_together=(
            ('room','booking_date','booking_time')
        )