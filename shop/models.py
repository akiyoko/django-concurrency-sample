from django.contrib.auth import get_user_model
from django.db import models
from concurrency.fields import AutoIncVersionField


User = get_user_model()


class Book(models.Model):
    """本モデル"""

    class Meta:
        db_table = 'book'
        verbose_name = verbose_name_plural = '本'

    title = models.CharField('タイトル', max_length=255, unique=True)
    price = models.PositiveIntegerField('価格', null=True, blank=True)

    def __str__(self):
        return self.title


class BookStock(models.Model):
    """在庫モデル"""

    class Meta:
        db_table = 'stock'
        verbose_name = verbose_name_plural = '在庫'

    book = models.OneToOneField(Book, verbose_name='本', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField('在庫数', default=0)
    updated_at = models.DateTimeField('更新日時', auto_now=True)
    version = AutoIncVersionField(verbose_name='バージョン')

    def __str__(self):
        return f'{self.book.title} ({self.quantity})'


class Order(models.Model):
    """注文モデル"""

    class Meta:
        db_table = 'order'
        verbose_name = verbose_name_plural = '注文'

    STATUS_PAYMENT_PROCESSING = '01'
    STATUS_PAYMENT_OK = '02'
    STATUS_PAYMENT_NG = '03'
    STATUS_PAYMENT_ERROR = '09'
    STATUS_CHOICES = (
        (STATUS_PAYMENT_PROCESSING, '決済中'),
        (STATUS_PAYMENT_OK, '決済OK'),
        (STATUS_PAYMENT_NG, '決済NG'),
        (STATUS_PAYMENT_ERROR, '決済エラー'),
    )

    status = models.CharField('ステータス', max_length=2, choices=STATUS_CHOICES)
    total_amount = models.PositiveIntegerField('金額合計')
    ordered_by = models.ForeignKey(User, verbose_name='注文者', on_delete=models.PROTECT,
                                   editable=False)
    ordered_at = models.DateTimeField('注文日時', auto_now_add=True)

    def __str__(self):
        return f'{self.get_status_display()} ({self.ordered_at:%Y-%m-%d %H:%M})'
