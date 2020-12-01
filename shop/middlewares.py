import logging

from django.db import connection

logger = logging.getLogger(__name__)


class DBAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # リクエストへの前処理
        self.process_request(request)

        response = self.get_response(request)

        # レスポンスへの後処理
        self.process_response(request, response)

        return response

    def process_request(self, request):
        """リクエストへの前処理"""
        # TODO
        with connection.cursor() as cursor:
            cursor.execute("SELECT 'This is process_request' FROM auth_user")

    def process_response(self, request, response):
        """レスポンスへの後処理"""
        # TODO
        with connection.cursor() as cursor:
            cursor.execute("SELECT 'This is process_response' FROM auth_user")

    def process_view(self, request, view_func, view_args, view_kwargs):
        """ビューを呼び出す直前に呼び出される処理"""
        # TODO
        with connection.cursor() as cursor:
            cursor.execute("SELECT 'This is process_view' FROM auth_user")
