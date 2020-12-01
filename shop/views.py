import logging

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction
# from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views import View

from .models import Book, BookStock, Order

logger = logging.getLogger(__name__)

User = get_user_model()


@method_decorator(transaction.non_atomic_requests, name='dispatch')
class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        book = get_object_or_404(Book, pk=kwargs['pk'])
        book_stock = get_object_or_404(BookStock, book=book)
        if book_stock.quantity == 0:
            messages.error(request, "在庫がないので購入できません。")
        context = {
            'book': book,
            'book_stock': book_stock,
        }
        return TemplateResponse(request, 'shop/checkout.html', context)

    def post(self, request, *args, **kwargs):
        # # TODO: ログイン状態をシミュレート
        # request.user = User(pk=1)

        book = get_object_or_404(Book, pk=kwargs['pk'])

        # 1) デフォルト
        # 2) ATOMIC_REQUESTS を有効化
        # # ① 注文情報を登録
        # order = Order(
        #     status=Order.STATUS_PAYMENT_PROCESSING,
        #     total_amount=book.price,
        #     ordered_by=request.user,
        # )
        # order.save()
        #
        # # ② 在庫数を確認
        # book_stock = get_object_or_404(BookStock, book=book)
        # # ③ 在庫数を1減らして更新
        # book_stock.quantity -= 1
        # book_stock.save()
        #
        # # 決済処理
        # try:
        #     print('決済処理')
        #     # TODO
        #     # raise Exception("決済処理で例外発生")
        # except Exception as e:
        #     # 在庫を1つ増やして更新
        #     book_stock = get_object_or_404(BookStock, book=book)
        #     book_stock.quantity += 1
        #     book_stock.save()
        #
        #     # 注文情報のステータスを更新
        #     order.status = Order.STATUS_PAYMENT_NG
        #     order.save()
        #
        #     messages.error(request, "決済NGです。")
        #     return TemplateResponse(request, 'shop/checkout_error.html')
        #
        # # ④ 注文情報のステータスを更新
        # order.status = Order.STATUS_PAYMENT_OK
        # order.save()

        # 3) transaction.atomic() で囲む
        # 4) ATOMIC_REQUESTS を有効化しているときに、特定のメソッド内で自前でトランザクションを切る
        with transaction.atomic():
            # ① 注文情報を登録
            order = Order(
                status=Order.STATUS_PAYMENT_PROCESSING,
                total_amount=book.price,
                ordered_by=request.user,
            )
            order.save()

            # ② 在庫数を確認
            book_stock = get_object_or_404(BookStock, book=book)
            # ③ 在庫数を1減らして更新
            book_stock.quantity -= 1
            book_stock.save()

        # ...（決済処理）...
        print('決済処理')

        with transaction.atomic():
            # ④ 注文情報のステータスを更新
            order.status = Order.STATUS_PAYMENT_OK
            order.save()

        messages.info(request, "購入しました。")
        if book_stock.quantity == 0:
            messages.warning(request, "在庫がなくなりました。")
        context = {
            'book': book,
            'book_stock': book_stock,
            'order': order,
        }
        return TemplateResponse(request, 'shop/checkout.html', context)
