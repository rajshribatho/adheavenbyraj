from django.contrib import admin

from .models import HomeTable, UserInfo, ListTable, OrderHistory

admin.site.register(HomeTable)
admin.site.register(UserInfo)
admin.site.register(ListTable)
admin.site.register(OrderHistory)
