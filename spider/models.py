from django.db import models


class BvInfo(models.Model):
    avid = models.IntegerField(primary_key=True, default=0, help_text="av号")
    bvid = models.CharField(max_length=32, help_text="bv号")
    title = models.CharField(max_length=128, help_text="标题")
    desc = models.TextField(help_text="简介")
    pages = models.IntegerField(default=1, help_text="视频分p数")
    ctime = models.IntegerField(default=0, help_text="视频投稿时间")
    pubdate = models.IntegerField(default=0, help_text="视频更新时间")
    duration = models.IntegerField(default=0, help_text="视频长度（s）")
    stat_view = models.IntegerField(default=0, help_text="播放数")
    stat_danmaku = models.IntegerField(default=0, help_text="弹幕数")
    stat_reply = models.IntegerField(default=0, help_text="评论数")
    stat_favorite = models.IntegerField(default=0, help_text="收藏数")
    stat_coin = models.IntegerField(default=0, help_text="投币数")
    stat_share = models.IntegerField(default=0, help_text="分享数")
    stat_like = models.IntegerField(default=0, help_text="喜欢数")

    own_mid = models.IntegerField(default=0, help_text="up主mid")
    own_name = models.CharField(max_length=128, help_text="up主昵称")
    db_update = models.DateTimeField(auto_now=True, help_text="数据更新时间")

    class Meta:
        db_table = "bv_info"
