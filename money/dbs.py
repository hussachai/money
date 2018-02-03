from django.db import connection
from django.db.models.functions import Coalesce
from money.models import *


def get_saving_goal(year):
    return AnnualGoal.objects.filter(year=year).values_list('target_saving', flat=True).get(pk=1)


def get_record_years():
    # return StmtBalance.objects.order_by('-closing_year')\
    #     .distinct().values_list('closing_year', flat=True)
    query = "SELECT DISTINCT closing_year FROM money_stmt_balances ORDER by closing_year DESC"
    with connection.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
    return [row[0] for row in rows]


def mode_to_field_proj(mode):
    if mode == "billed":
        return "sb.closing_date"
    elif mode == "due":
        return "sb.due_date"
    else:
        return "sd.tx_date"


def get_statement_summary(year, month=None, mode="purchased"):
    extra_cond = ""
    if month is not None:
        extra_cond = "AND s.c_month = %s"
    prj_field = mode_to_field_proj(mode)

    query = f"""
        SELECT s.c_year, s.c_month, s.category_name, s.category_color, SUM(s.sum_amount) AS total FROM
        (
            (
                SELECT s.c_year, s.c_month, c.id AS category_id, c.name AS category_name, 
                c.color AS category_color, SUM(s.amount) * -1 AS sum_amount FROM
                (SELECT YEAR({prj_field}) AS c_year, MONTH({prj_field}) AS c_month, sd.category_id, sd.amount 
                    FROM money_stmt_details sd JOIN money_stmt_balances sb ON sd.balance_id = sb.id
                    WHERE sb.closing_year = %s
                ) s 
                JOIN money_categories c ON s.category_id = c.id
                WHERE c.cat_type <> 0
                GROUP BY c_year, c_month, s.category_id
            )
            UNION
            (
                SELECT YEAR(stmt.tx_date) AS c_year, MONTH(stmt.tx_date) AS c_month, 
                c.id AS category_id, c.name AS category_name, c.color AS category_color, SUM(stmt.amount) AS sum_amount
                FROM money_income_stmts stmt JOIN money_categories c ON stmt.category_id = c.id
                WHERE c.cat_type <> 0 AND stmt.tx_year = %s
                GROUP BY c_year, c_month, stmt.category_id
            )
        ) s
        WHERE c_year = %s {extra_cond}
        GROUP BY  s.c_year, s.c_month, s.category_name, s.category_color
        ORDER BY s.c_month DESC, total DESC
    """

    with connection.cursor() as cursor:
        if month is not None:
            cursor.execute(query, [year, year, year, month])
        else:
            cursor.execute(query, [year, year, year])

        row = fetchall_as_dict(cursor)

    return row


def get_statement_details(year, month, mode):
    prj_field = mode_to_field_proj(mode)
    query = f"""
      SELECT * FROM
      (
        (
            SELECT 'C' AS tx_type, sd.id AS tx_id, ca.name AS account_name, sd.tx_date, sb.closing_date, sb.due_date, c.name AS category, sd.amount 
            FROM money_stmt_details sd 
            JOIN money_stmt_balances sb ON sd.balance_id = sb.id
            JOIN money_credit_accounts ca ON sb.account_id = ca.id
            JOIN money_categories c ON sd.category_id = c.id
            WHERE {prj_field} >= '%s-01-01' AND {prj_field} < '%s-01-01' AND month({prj_field}) = %s AND c.cat_type <> 0
        )
        UNION
        (
          SELECT 'D' AS tx_type, mis.id AS tx_id, ba.name AS account_name, mis.tx_date, mis.tx_date AS closing_date, 
            mis.tx_date AS due_date, c.name AS category, mis.amount 
          FROM money_income_stmts mis 
          JOIN money_bank_accounts ba ON mis.account_id = ba.id
          JOIN money_categories c ON mis.category_id = c.id
          WHERE mis.tx_date >= '%s-01-01' AND mis.tx_date < '%s-01-01' AND month(mis.tx_date) = %s AND c.cat_type <> 0
        )
      ) acc
      ORDER BY acc.tx_date;
    """
    with connection.cursor() as cursor:
        next_year = int(year) + 1
        params = [int(year), next_year, month] * 2
        print(params)
        cursor.execute(query, params)
        row = fetchall_as_dict(cursor)
    return row


def fetchall_as_dict(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

