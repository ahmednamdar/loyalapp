from django.contrib import admin
from django.urls import reverse_lazy
from core.forms import OrderAdminForm
from core.models import customer, Group, Order
from django.utils.html import format_html


# Register your models here.


class MyUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'identity',
                    'credit', 'birthday', 'my_url_field', 'send', 'history')
    search_fields = ['first_name', 'identity']

    def my_url_field(self, obj):
        return format_html(f'<a href="{reverse_lazy("print id", kwargs={"id":obj.identity})}" class="btn btn-primary">print</a>')
    my_url_field.allow_tags = True
    my_url_field.short_description = 'actions'

    def send(self, obj):
        return format_html(f'<a href="{reverse_lazy("send", kwargs={"phone_number":obj.phone_number})}" class="btn btn-primary">Send</a>')
    send.allow_tags = True
    send.short_description = 'actions'

    def history(self, obj):
        return format_html(f'<a href="{reverse_lazy("history", kwargs={"id":obj.identity})}" class="btn btn-primary">History</a>')


admin.site.register(customer, MyUserAdmin)


class GroupCore(admin.ModelAdmin):

    pass


admin.site.register(Group, GroupCore)
# class OrderItemAdmin(admin.ModelAdmin):
#   list_display = ('product','total')
#  pass
#
#
#
# admin.site.register(OrderItem,OrderItemAdmin)


class OrderAdmin(admin.ModelAdmin):
    form = OrderAdminForm
    list_display = ('customer', 'totalPrice')

    change_form_template = 'admin/mymodel_change_form.html'
    pass


admin.site.register(Order, OrderAdmin)


admin.site.site_header = "Bayt Halab"
admin.site.site_title = "Bayt Halab"
