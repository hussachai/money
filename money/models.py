
import datetime
from django.db import models
from django.db.models import Sum
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.html import format_html
from django.db.models.signals import pre_save
from colorfield.fields import ColorField
from money.utils import random_color

# Create your models here.

class CreditAccount(models.Model):
    name = models.CharField(max_length=64)
    opened_date = models.DateField(auto_now=False)
    closed_date = models.DateField(auto_now=False, null=True, blank=True)

    def __str__(self):
        return self.name

    def account_status_html(self):
        if self.closed_date and self.closed_date <= timezone.now().date():
            return format_html('<span style="color: #DC143C;">Closed</span>')
        else:
            return format_html('<span style="color: #6495ED;">Active</span>')

    class Meta:
        db_table = 'money_credit_accounts'
        unique_together = ('name', 'opened_date',)
        ordering = ['closed_date', 'name', 'opened_date']
        verbose_name = 'Credit Account'
        verbose_name_plural = 'Credit Accounts'


class StmtBalance(models.Model):
    account = models.ForeignKey(CreditAccount)
    closing_date = models.DateField(auto_now=False)
    closing_year = models.SmallIntegerField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    due_date = models.DateField(auto_now=False)

    def __str__(self):
        return '%s - %s' % (self.account.name, self.closing_date, )

    def save(self, *args, **kwargs):
        self.closing_year = self.closing_date.year
        super(StmtBalance, self).save(*args, **kwargs)

    def was_issued_recently(self):
        return self.closing_date >= timezone.now() - datetime.timedelta(days=1)

    def diff_amount(self):
        return self.amount - self.stmtdetail_set.aggregate(Sum('amount'))['amount__sum']

    class Meta:
        db_table = 'money_stmt_balances'
        unique_together = ('account', 'closing_date',)
        ordering = ['-closing_date', 'account']
        verbose_name = 'Statement Balance'
        verbose_name_plural = 'Statements Balance'

class StmtBalanceSummary(StmtBalance):
    class Meta:
        proxy = True
        verbose_name = 'Statement Summary'
        verbose_name_plural = 'Statements Summary'


class Category(MPTTModel):
    CATEGORY_TYPES = (
        (-1, 'Expense'),
        (0, 'Transfer/Payment'),
        (1, 'Income')
    )
    name = models.CharField(max_length=64)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)
    cat_type = models.SmallIntegerField(choices=CATEGORY_TYPES)
    color = ColorField(default=random_color())
    note = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return '%s: %s' % (self.name, dict(self.CATEGORY_TYPES)[self.cat_type], )

    class Meta:
        db_table = 'money_categories'
        unique_together = ('name', 'parent',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    class MPTTMeta:
        order_insertion_by = ['name']

class StmtDetail(models.Model):
    balance = models.ForeignKey(StmtBalance)
    tx_date = models.DateField(auto_now=False)
    category = models.ForeignKey(Category)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    note = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return '%s ($%s)' % (self.category.name, self.amount, )

    class Meta:
        db_table = 'money_stmt_details'
        ordering = ['-balance__closing_date', '-tx_date']
        verbose_name = 'Statement Detail'
        verbose_name_plural = 'Statements Detail'

class BankAccount(models.Model):
    ACCOUNT_TYPES = (
        ('C', 'Checking'),
        ('S', 'Saving')
    )
    name = models.CharField(max_length=64)
    account_type = models.CharField(max_length=1, choices=ACCOUNT_TYPES)
    remaining_balance = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'money_bank_accounts'
        unique_together = ('name', 'account_type',)
        verbose_name = 'Bank Account'
        verbose_name_plural = 'Bank Accounts'

class IncomeStmt(models.Model):
    account = models.ForeignKey(BankAccount)
    category = models.ForeignKey(Category)
    tx_date = models.DateField(auto_now=False)
    tx_year = models.SmallIntegerField()
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    linked_account = models.ForeignKey(CreditAccount, blank=True, null=True)
    note = models.CharField(max_length=128, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.tx_year = self.tx_date.year
        super(IncomeStmt, self).save(*args, **kwargs)

    def item_name(self):
        return '%s - %s' % (self.account.name, self.category,)

    class Meta:
        db_table = 'money_income_stmts'
        ordering = ['-tx_date', 'account']
        verbose_name = 'Income Statement'
        verbose_name_plural = 'Income Statements'

class AnnualGoal(models.Model):
    year = models.SmallIntegerField()
    target_saving = models.DecimalField(max_digits=10, decimal_places=2)

    def montly_goal(self):
        return round(self.target_saving / 12, 2)

    def __str__(self):
        return 'Goal: %s - $%s' % (self.year, self.target_saving)

    class Meta:
        db_table = 'money_annual_goals'
        ordering = ['-year']
        verbose_name = 'Annual Goal'
        verbose_name_plural = 'Annual Goals'

