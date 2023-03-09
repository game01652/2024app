# Copyright 2022 Kokai Sakaguchi
# モデル models.py

from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.core.validators import MaxValueValidator, MinValueValidator


# 「ステージ」クラス
class Stage(models.Model):
    title = models.CharField(
        verbose_name = 'Stage',
        blank = True,
        null = True,
        max_length = 255,
    )

    def __str__(self):
        return self.title


# 「カテゴリー」クラス
class Category(models.Model):
    title = models.CharField(
        verbose_name = 'Category',
        blank = True,
        null = True,
        max_length = 255,
    )

    def __str__(self):
        return self.title


# 「言語」クラス
class Language(models.Model):
    title = models.CharField(
        verbose_name = 'Language',
        blank = True,
        null = True,
        max_length = 255,
    )

    def __str__(self):
        return self.title


# 「書籍」クラス
class Book(models.Model):
    # タイトル
    title = models.CharField(
        verbose_name = 'Title',
        blank = True,
        null = True,
        max_length = 255,
    )

    # 著者
    author = models.CharField(
        verbose_name = 'Author',
        blank = True,
        null = True,
        max_length = 255,
    )

    # 出版年月日
    publishedDate = models.CharField(
        verbose_name='PublishedDate',
        blank = True,
        null = True,
        max_length = 255,
    )

    # あらすじ
    description = models.TextField(
        verbose_name = 'Description',
        blank = True,
        null = True,
        max_length = 1000,
    )
    
    # ISBN
    isbn = models.CharField(
        verbose_name = 'ISBN',
        blank = True,
        null = True,
        max_length = 255,
    )

    # ページ数
    page = models.IntegerField(
        verbose_name = 'Page',
        blank = True,
        null = True,
        validators = [    # 下限。
            MinValueValidator(0)
        ]
    )

    # 表紙画像
    bookCover = models.ImageField(
        verbose_name = 'BookCover',
        blank = True,
        null = True,
        upload_to = 'images/',    # 画像の保存フォルダ。
    )

    # 登録年月日
    registerDate = models.DateTimeField(
        verbose_name = 'RegisterDate',
        blank = True,
        null = True,
        default = datetime.now(),    # 登録時に自動付与。
    )

    # 更新年月日
    updateDate = models.DateTimeField(
        verbose_name = 'UpdateDate',
        blank = True,
        null = True,
        auto_now = True,           # 更新時に自動付与。
    )

    # 感想
    impression = models.TextField(
        verbose_name = 'Impression',
        blank = True,
        null = True,
        max_length = 1000,
    )

    # レビュー数
    review = models.IntegerField(
        verbose_name = 'Review',
        blank = True,
        null = True,
        validators = [    # 下限・上限。
            MinValueValidator(1), MaxValueValidator(5)
        ]
    )

    # 何冊目に読んだ書籍か。
    order = models.IntegerField(
        verbose_name = 'Order',
        blank = True,
        null = True,
    )

    # ユーザ
    user = models.ForeignKey(
        User, 
        on_delete = models.CASCADE,    # ユーザを削除した場合、書籍が削除される。
        verbose_name = 'User',
        blank = True,
        null = True,
    )

    # カテゴリー
    category = models.ForeignKey(
        Category,
        on_delete = models.SET_NULL,    # カテゴリーを削除した場合、NULLが設定される。
        verbose_name = 'Category',
        blank = True,
        null = True,
    )

    # 言語
    language = models.ForeignKey(
        Language,
        on_delete = models.SET_NULL,    # 言語を削除した場合、NULLが設定される。
        verbose_name = 'Language',
        blank = True,
        null = True,
    )

    # 進捗段階
    stage = models.ForeignKey(
        Stage,
        on_delete=models.SET_NULL,    # 進捗段階を削除した場合、NULLが設定される。
        verbose_name = 'Stage',
        null = True,
        blank = True,
    )

    def __str__(self):
        return self.title
