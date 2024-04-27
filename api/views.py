#rest framework
import csv
import datetime
from io import TextIOWrapper
import traceback
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

#models
from api.models import entries
from django.db.models import Max


#serializers
from api.serializers import EntriesSerializer

#custom utils
from api.utils.cash_balance_calculator import calcute_cash_in_hand


class ViewCashbookEntries(APIView):
    def get(self, request):
        try:
            entry = entries.objects.all().order_by('date')
            
            if entry:
                serializer = EntriesSerializer(entry, many=True)
                return Response({
                    "Success": True,
                    "Message": "Entries Fetched successfully.",
                    "Data": serializer.data,
                    "Status": status.HTTP_200_OK
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "Success": False,
                    "Message": "No Entries available",
                    "Data": '',
                    "Status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            return Response({
                "Success": False,
                "Message": "Error Occurred",
                "Status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Data": str(error)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class AddCashbookEntry(APIView):
    def post(self, request):

        date = request.POST['date']
        type_of_entry = (request.POST['type_of_entry']).upper()
        type_of_entry_allowed = ['RECEIPT', 'PAYMENT']
        if type_of_entry not in type_of_entry_allowed:
            return Response({
                    "Success": False,
                    "Message": "Invalid Type of Entry, Should be among these [receipt or payment]",
                    "Data": '',
                    "Status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST)
        
        particulars = request.POST['particulars']
        detail = request.POST['detail']
        amount = request.POST['amount']
        cash = 0
        
        if not particulars or not detail or not date or not amount:
            return Response({
                    "Success": False,
                    "Message": "Input Data Missing from user",
                    "Data": '',
                    "Status": status.HTTP_400_BAD_REQUEST
                }, status=status.HTTP_400_BAD_REQUEST) 
        amount = int(amount)
        date_format = "%Y-%m-%d"  
        try:
            date_object = datetime.datetime.strptime(date, date_format).date()
            max_date_of_entry = entries.objects.aggregate(max_date=Max('date'))['max_date']
        
            if max_date_of_entry is None:
                max_date_of_entry = date_object
            if date_object < max_date_of_entry:
                al_entries_of_same_date = entries.objects.filter(date=date_object)
                al_entries_of_earlier_date = entries.objects.filter(date__lt=date_object).order_by('date')
                len_of_all_same_date_entries = len(al_entries_of_same_date)
                len_of_all_earlier_date_entries = len(al_entries_of_earlier_date)

                
                if len_of_all_same_date_entries:
                    print('inside if')
                    al_same_date_entries = al_entries_of_same_date[len_of_all_same_date_entries-1]
                    if type_of_entry == 'RECEIPT':
                        cash = al_same_date_entries.cash + amount
                    else:
                        cash = al_same_date_entries.cash - amount
                    
                elif len_of_all_same_date_entries == 0 and len_of_all_earlier_date_entries == 0:
                    print('inside elif')
                    if type_of_entry == 'RECEIPT':
                        cash = amount
                    else:
                        cash = -1 * amount

                else:
                    print('inside else')
                    al_earlier_entries = len_of_all_earlier_date_entries[len_of_all_earlier_date_entries-1]
                    if type_of_entry == 'RECEIPT':
                        cash = al_earlier_entries.cash + amount
                    else:
                        cash = al_earlier_entries.cash - amount
                    
                entries.objects.create(date=date,type_of_entry=type_of_entry,particulars=particulars,detail=detail,amount=amount,cash=cash)
                latest_entry = entries.objects.last()
                latest_entry_details = entries.objects.get(id=latest_entry.id)
                latest_entry_details.cash = cash
                latest_entry_details.save()
                al_entries_after_date = entries.objects.filter(date__gt=date_object)
                for entry in al_entries_after_date:
                    if type_of_entry == 'RECEIPT':
                        old_cash = entry.cash
                        new_cash = old_cash + amount
                    else:
                        old_cash = entry.cash
                        new_cash = old_cash - amount
                    after_date_entry_details = entries.objects.get(id=entry.id)
                    after_date_entry_details.cash = new_cash
                    after_date_entry_details.save()
                serializer = EntriesSerializer(latest_entry_details)
                return Response({
                    "Success": True,
                    "Message": "Entry Added successfully.",
                    "Data": serializer.data,
                    "Status": status.HTTP_200_OK
                }, status=status.HTTP_200_OK)

            else:
                print('else')
                entries.objects.create(date=date,type_of_entry=type_of_entry,particulars=particulars,detail=detail,amount=amount,cash=cash)
                upd = entries.objects.last()
                upd_obj = entries.objects.get(id=upd.id)
                print(upd_obj.cash)
                cash = calcute_cash_in_hand(request)
                print(cash)
                upd_obj.cash = cash
                upd_obj.save()

                serializer = EntriesSerializer(upd_obj)

                return Response({
                    "Success": True,
                    "Message": "Entry Added successfully.",
                    "Data": serializer.data,
                    "Status": status.HTTP_200_OK
                }, status=status.HTTP_200_OK)
        except Exception as error:
            traceback.print_exc()
            return Response({
                    "Success": False,
                    "Message": "Internal server error",
                    "Data": '',
                    "Status": status.HTTP_500_INTERNAL_SERVER_ERROR
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


class DeleteEntry(APIView):
    def post(self, request):
        try:
            entryiddel = request.POST.get('entryid') #will give value None if key is not present in post data.
            print(entryiddel)
            del_obj = entries.objects.get(id=entryiddel)
            del_date = del_obj.date
            before_date_cih = entries.objects.filter(date__lt=del_date)
            after_date_cih = entries.objects.filter(date__gt=del_date)
            same_date = entries.objects.filter(date=del_date).exclude(id=entryiddel)
            
            
            if len(same_date) > 0:
                for dts in same_date:
                    print(dts.id)
                    if del_obj.type_of_entry == 'RECEIPT':
                        print(dts.cash, '-', del_obj.amount)
                        dts.cash = dts.cash - del_obj.amount
                        dts.save()
                    else:
                        print(dts.cash, '+', del_obj.amount)
                        dts.cash = dts.cash + del_obj.amount
                        dts.save()
            if not before_date_cih:
                print('inside')
                print(del_obj.amount)
                for dts in after_date_cih:
                    if del_obj.type_of_entry == 'RECEIPT':
                        print(dts.cash,'-',del_obj.amount)
                        dts.cash = dts.cash - del_obj.amount
                        dts.save()
                    else:
                        print(dts.cash,'+',del_obj.amount)
                        dts.cash = dts.cash + del_obj.amount
                        dts.save()

            else:
                for dts in after_date_cih:
                    if del_obj.type_of_entry == 'RECEIPT':
                        print(dts.date,dts.cash, '-', del_obj.amount)
                        dts.cash = dts.cash - del_obj.amount
                        dts.save()
                    else:
                        print(dts.date,dts.cash, '+', del_obj.amount)
                        dts.cash = dts.cash + del_obj.amount
                        dts.save()
            del_obj.delete()
            entry = entries.objects.all().order_by('date')
            
            if entry:
                serializer = EntriesSerializer(entry, many=True)
                return Response({
                            "Success": True,
                            "Message": "Entry Deleted succesfully",
                            "Data": serializer.data,
                            "Status": status.HTTP_200_OK
                        },status=status.HTTP_200_OK
                        )
            else:
                return Response({
                            "Success": True,
                            "Message": "Entry Deleted succesfully",
                            "Data": 'No entries available now.',
                            "Status": status.HTTP_200_OK
                        },status=status.HTTP_200_OK
                        )
        

        except entries.DoesNotExist as error:
                return Response({
                        "Success": False,
                        "Message": "Invalid Entry, does not exists.",
                        "Data": '',
                        "Status": status.HTTP_400_BAD_REQUEST
                    }, status=status.HTTP_400_BAD_REQUEST)
        

        except Exception as e:
                traceback.print_exc()
                
                return Response({
                    "Success": False,
                    "Message": "Internal server error",
                    "Data": str(e),
                    "Status": status.HTTP_500_INTERNAL_SERVER_ERROR
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class UpdateEntry(APIView):
    def post(self, request, entryid):
        try:
            upd_obj = entries.objects.get(id=entryid)
            dates = request.POST['date']
            typetxn = request.POST.get('type').upper()
            particulars = request.POST.get('particulars')
            detail = request.POST.get('detail')
            amount = request.POST.get('amount')
            print(dates)
            upd_obj.date = dates
            upd_obj.type_of_entry = typetxn
            upd_obj.particulars = particulars
            upd_obj.amount = amount
            upd_obj.detail = detail
            upd_obj.save()

            date_obj = datetime.datetime.strptime(dates, '%Y-%m-%d')

            new_cash_date = (date_obj - datetime.timedelta(days=1)).date()
            payments = entries.objects.filter(type_of_entry='PAYMENT')
            tlistpay = []
            for pay in payments:
                totallist = tlistpay.append(pay.amount)
            print(tlistpay)
            payments_total = sum(tlistpay)

            receipts = entries.objects.filter(type_of_entry='RECEIPT')
            tlistrec = []
            for pay in receipts:
                totallist = tlistrec.append(pay.amount)
            print(tlistrec)
            receipts_total = sum(tlistrec)

            cash1 = receipts_total - payments_total

            print(cash1)
            
            upd = entries.objects.last()
            print(upd.cash)
            upd.cash = cash1
            upd.save()
            
            serializer = EntriesSerializer(upd_obj)
            return Response({
                            "Success": True,
                            "Message": "Entry Updated succesfully",
                            "Data": serializer.data,
                            "Status": status.HTTP_200_OK
                        },status=status.HTTP_200_OK
                        )
        

        except entries.DoesNotExist as error:
                return Response({
                        "Success": False,
                        "Message": "Invalid Entry, does not exists.",
                        "Data": '',
                        "Status": status.HTTP_400_BAD_REQUEST
                    }, status=status.HTTP_400_BAD_REQUEST)
        


        except Exception as e:
            traceback.print_exc()

            return Response({
                    "Success": False,
                    "Message": "Internal server error",
                    "Data": str(e),
                    "Status": status.HTTP_500_INTERNAL_SERVER_ERROR
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



                #----------------------------------Ledger Views------------------------------------#


class Ledger(APIView):
    def get(self, request):
        try:
            non_repeated_names = entries.objects.values_list('particulars', flat=True).distinct()
            if non_repeated_names:
                bals = []
                ledger_list = []
                for names in non_repeated_names:
                    payments = entries.objects.filter(type_of_entry='PAYMENT',particulars=names)
                    tlistpay = []
                    for pay in payments:
                        totallist = tlistpay.append(pay.amount)
                    payments_total = sum(tlistpay)
                    receipts = entries.objects.filter(type_of_entry='RECEIPT',particulars=names)

                    tlistrec = []
                    for pay in receipts:
                        totallist = tlistrec.append(pay.amount)
                    receipts_total = sum(tlistrec)

                    cash1 = receipts_total - payments_total
                    bals.append(cash1)
                
                account_head_with_balance = list(zip(non_repeated_names, bals))
                
                for account_head, balance in account_head_with_balance:
                    ledger_data = {
                        'account_head': account_head,
                        'balance': balance 
                    }
                    ledger_list.append(ledger_data)
                
                return Response({
                                    "Success": True,
                                    "Message": "Ledger retrieved succesfully.",
                                    "Data": ledger_list,
                                    "Status": status.HTTP_200_OK
                                },status=status.HTTP_200_OK
                                )
            
            else:
                return Response({
                                    "Success": True,
                                    "Message": "No Entries available to display.",
                                    "Data": '',
                                    "Status": status.HTTP_200_OK
                                },status=status.HTTP_200_OK
                                )
        
        
        except Exception as internal:
            traceback.print_exc()
            return Response({
                    "Success": False,
                    "Message": "Internal server error",
                    "Data": str(internal),
                    "Status": status.HTTP_500_INTERNAL_SERVER_ERROR
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class LedgerAccount(APIView):
    def get(self, request, particulars):
        try:
            paricular_account = entries.objects.filter(particulars=particulars).order_by('date')
            payments = entries.objects.filter(type_of_entry='PAYMENT',particulars=particulars)
            tlistpay = []
            for pay in payments:
                totallist = tlistpay.append(pay.amount)
            payments_total = sum(tlistpay)
            receipts = entries.objects.filter(type_of_entry='RECEIPT',particulars=particulars)
            tlistrec = []
            for pay in receipts:
                totallist = tlistrec.append(pay.amount)
            receipts_total = sum(tlistrec)
            cash1 = receipts_total - payments_total
            p_cash = []
            neg_check = []
            if paricular_account[0].type_of_entry == 'PAYMENT':
                cash = -1 * paricular_account[0].amount
                p_cash.append(cash)
            else:
                cash = paricular_account[0].amount
                p_cash.append(cash)
            y = len(paricular_account)
            for ent in range(1,y):
                if paricular_account[ent].type_of_entry == 'RECEIPT':
                    cash = p_cash[-1] + paricular_account[ent].amount
                    p_cash.append(cash)
                else:
                    if p_cash[-1] < 0:  
                        cash = p_cash[-1] - paricular_account[ent].amount
                    else:
                        cash = p_cash[-1] + paricular_account[ent].amount
                    p_cash.append(cash)
            for ch in p_cash:
                if ch < 0:
                    neg_check.append(False)
                else:
                    neg_check.append(True)

            serialized_data = EntriesSerializer(paricular_account, many=True)

            ledger_account_data = {
                'account': serialized_data.data,
                'cashp': cash1,
                'particulars': particulars,
                'receipts_total': receipts_total,
                'payments_total': payments_total
            }


            return Response({
                                    "Success": True,
                                    "Message": "Ledger Account retrieved succesfully.",
                                    "Data": ledger_account_data,
                                    "Status": status.HTTP_200_OK
                                },status=status.HTTP_200_OK
                                )

        
        except Exception as internal:
            traceback.print_exc()
            return Response({
                    "Success": False,
                    "Message": "Internal server error",
                    "Data": str(internal),
                    "Status": status.HTTP_500_INTERNAL_SERVER_ERROR
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



def add_bulk_entries_util(params):
    try:
        date = params['date']
        print(date)
        type_of_entry = params['type_of_entry'].upper()
        particulars = params['particulars']
        detail = params['detail']
        amount = int(params['amount'])
        cash = 0
        date_format = "%d-%m-%Y" # Adjust the format based on your date string
        date_object = date
        max_date_of_entry = entries.objects.aggregate(max_date=Max('date'))['max_date']

        if max_date_of_entry is None:
            max_date_of_entry = date_object
        if date_object < max_date_of_entry:
            try:
                al_objs_earlier = entries.objects.filter(date=date_object)
                al_objs_earlier_b = entries.objects.filter(date__lt=date_object).order_by('date')
                l = len(al_objs_earlier)
                l2 = len(al_objs_earlier_b)

            except Exception as e:
                print(e)
            print(l,l2)
            if al_objs_earlier:
                al_objs_earlier = al_objs_earlier[l-1]
                if type_of_entry == 'RECEIPT':
                    cash = al_objs_earlier.cash + amount
                else:
                    cash = al_objs_earlier.cash - amount
            elif l == 0 and l2 == 0:
                print('inside elif')
                print(type_of_entry)
                if type_of_entry == 'RECEIPT':
                    cash = amount
                else:
                    cash = -1 * amount
            else:
                al_objs_earlier = al_objs_earlier_b[l2-1]
                if type_of_entry == 'RECEIPT':
                    cash = al_objs_earlier.cash + amount
                else:
                    cash = al_objs_earlier.cash - amount
                
            entries.objects.create(date=date,type_of_entry=type_of_entry,particulars=particulars,detail=detail,amount=amount,cash=cash)
            upd = entries.objects.last()
            upd_obj = entries.objects.get(id=upd.id)
            print(cash)
            upd_obj.cash = cash
            upd_obj.save()
            al_objs = entries.objects.filter(date__gt=date_object)
            for al in al_objs:
                if type_of_entry == 'RECEIPT':
                    old_cash = al.cash
                    new_cash = old_cash + amount
                else:
                    old_cash = al.cash
                    new_cash = old_cash - amount
                upd_obj = entries.objects.get(id=al.id)
                upd_obj.cash = new_cash
                upd_obj.save()

        else:
            entries.objects.create(date=date,type_of_entry=type_of_entry,particulars=particulars,detail=detail,amount=amount,cash=cash)
            upd = entries.objects.last()
            upd_obj = entries.objects.get(id=upd.id)
            print(upd_obj.cash)
            cash = calcute_cash_in_hand()
            upd_obj.cash = cash
            upd_obj.save()

        return True
        
    except Exception as internal:
        traceback.print_exc()
        return False
    
   
class AddBulkEntries(APIView):
    def post(self, request):
        try:
            csv_file = request.FILES.get('csv_file')
            csv_file_data = []
            date_format = "%d-%m-%Y"
            inserted_data_list = []
            if csv_file:
                uploaded_file_wrapper = TextIOWrapper(csv_file.file, encoding='utf-8')
                print(type(uploaded_file_wrapper))
                reader = csv.reader(uploaded_file_wrapper)

                next(reader, None)
                for row in reader:
                    print(row)
                    date = datetime.datetime.strptime(row[0], date_format).date()
                    type_of_entry = row[1]
                    particulars = row[2]
                    detail = row[3]
                    amount = row[4]
                    data = {'date': date, 'type_of_entry': type_of_entry, 'particulars': particulars, 'detail': detail, 'amount': amount}
                    inserted_data_list.append(data)
                    add_entries = add_bulk_entries_util(data)
                if add_entries:
                    print('done')
                    return Response({
                        "success": True,
                        "message": "Added Entries successfully",
                        "status_code": status.HTTP_200_OK,
                        "data": inserted_data_list
                    }, status=status.HTTP_200_OK
                    )
                else:
                    return Response({
                        "success": False,
                        "message": "Bad Request.",
                        "status_code": status.HTTP_400_BAD_REQUEST,
                        "data": ""
                    }, status=status.HTTP_400_BAD_REQUEST
                    )
        except Exception as error:
            print(error)
            return Response({
                        "success": False,
                        "message": "Internal server error.",
                        "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                        "data": ""
                    },status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )