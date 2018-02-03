from django.contrib import admin

# Register your models here.
from mptt.admin import DraggableMPTTAdmin
from .models import *
from django.db.models import Sum, Count

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'account_type', 'remaining_balance')

    def save_model(self, request, obj, form, change):
        # IncomeStmt.objects.get_or_create()
        super().save_model(request, obj, form, change)

@admin.register(CreditAccount)
class CreditAccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'opened_date', 'closed_date', 'account_status_html')

class StmtDetailInline(admin.TabularInline):
    model = StmtDetail
    extra = 5

@admin.register(StmtBalance)
class StmtBalanceAdmin(admin.ModelAdmin):
    list_display = ('account', 'closing_date', 'due_date', 'amount', 'diff_amount')
    list_display_links = ('account', 'closing_date')
    search_fields = ('account__name', 'closing_date',)
    inlines = [StmtDetailInline]

@admin.register(StmtBalanceSummary)
class StmtBalanceSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/stmt_balance_summary_change_list.html'
    date_hierarchy = 'due_date'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )
        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
        'total': Count('id'),
        'total_amount': Sum('amount'),
        }
        response.context_data['summary'] = list(
            qs.values('account__name')
            .annotate(**metrics)
            .order_by('-total_amount')
        )
        return response


@admin.register(StmtDetail)
class StmtDetailAdmin(admin.ModelAdmin):
    fields = ['balance', 'tx_date', 'category', 'amount', 'note']
    list_display = ('balance', 'category', 'tx_date', 'amount')
    list_display_links = None
    raw_id_fields = ("balance", 'category',)

@admin.register(IncomeStmt)
class IncomeStmtAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'tx_date', 'amount')
    # list_display_links = None

    def save_model(self, request, obj, form, change):
        if obj.category.cat_type == -1 and obj.amount > 0:
            obj.amount *= -1
        super().save_model(request, obj, form, change)

@admin.register(AnnualGoal)
class IncomeStmtAdmin(admin.ModelAdmin):
    list_display = ('year', 'target_saving', 'montly_goal')

    # def year_str(self, obj):
    #     return str(obj.year)

admin.site.register(Category, DraggableMPTTAdmin)

admin.site.site_title = 'My Money Admin'
admin.site.site_header = 'My Money Admin'
