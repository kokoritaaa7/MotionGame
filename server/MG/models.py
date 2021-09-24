from django.db import models

# Create your models here.
class RankingBoard(models.Model):
    name = models.CharField(max_length=10, help_text='10자 이하만 입력 가능')              # 입력받을 사용자 이름
    score = models.IntegerField()                       # 점수 
    date = models.DateTimeField(auto_now_add=True)      # Score에 등록된 시간 (해당 레코드 생성 시 현재 시간 자동 저장)
