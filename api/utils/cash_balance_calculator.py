from api.models import entries


def calcute_cash_in_hand(request):
    payments_list = []
    receipts_list = []
    payments = entries.objects.filter(type_of_entry='PAYMENT')
    for pay in payments:
        payments_list.append(pay.amount)
    payments_total = sum(payments_list)

    receipts = entries.objects.filter(type_of_entry='RECEIPT')
    for pay in receipts:
        receipts_list.append(pay.amount)
    receipts_total = sum(receipts_list)

    cash = receipts_total - payments_total

    return cash