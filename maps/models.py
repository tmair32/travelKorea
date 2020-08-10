from django.db import models
from myaccounts.models import MyUser

# Create your models here.
class Common(models.Model):
    contentId = models.IntegerField(unique=True)
    sigungu = models.IntegerField(null=True)
    area = models.IntegerField(null=True)
    mapx = models.FloatField(null=True)
    mapy = models.FloatField(null=True)
    category = models.IntegerField(null=True)
    title = models.TextField(null=True)
    tel = models.TextField(null=True)
    overview = models.TextField(null=True)
    addr1 = models.TextField(null=True)
    addr2 = models.TextField(null=True)
    homepage = models.TextField(null=True)
    avgScore = models.FloatField(null=True)
    zipCode = models.TextField(null=True)
    image = models.TextField(null=True)

    def __str__(self):
       return self.title

class Detail(models.Model):
    detailId = models.IntegerField()
    common = models.ForeignKey(Common, on_delete=models.CASCADE)
    startTime = models.TextField(null=True)
    endTime = models.TextField(null=True)
    parking = models.TextField(null=True)
    chkPet = models.TextField(null=True)
    chkBaby = models.TextField(null=True)
    restDate = models.TextField(null=True)
    useTime = models.TextField(null=True)
    ageLimit =  models.TextField(null=True)
    pay = models.TextField(null=True)
    barbeque = models.TextField(null=True)
    refund = models.TextField(null=True)
    subevent = models.TextField(null=True)
    openPeriod = models.TextField(null=True)
    discountInfo = models.TextField(null=True)
    chkCook = models.TextField(null=True)
    openTime = models.TextField(null=True)
    chkPack = models.TextField(null=True)
    chkSmoking = models.TextField(null=True)
    infoCenter = models.TextField(null=True)

class Bookmark(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    inform = models.ForeignKey(Common, on_delete=models.CASCADE)
    contentType = models.IntegerField(default=0)

    class Meta:
        unique_together = ("user", "inform")


class Stamp(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    inform = models.ForeignKey(Common, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "inform")

class Comment(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    inform = models.ForeignKey(Common, on_delete=models.CASCADE)
    content = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    contentId = models.IntegerField(default=0)

    def __str__(self):
       return '%s %s'%(self.user, self.content)

    class Meta:
        unique_together = ("id", "user", "contentId")

CHOICES = [(i,i) for i in range(1, 6)]

class Score(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    inform = models.ForeignKey(Common, on_delete=models.CASCADE, null=True)
    score = models.IntegerField(choices=CHOICES, null=True)
    content = models.TextField(default="", null=True)
    contentId = models.IntegerField(default=0)

    class Meta:
        unique_together = ("user", "inform")