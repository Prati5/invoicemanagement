from django.http.response import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from .models import Invoice,Transaction
from .serializer import InvoiceSerializer
from rest_framework.response import Response

class InvoiceView(APIView):

    def get_object(self, pk):
        try:
            return Invoice.objects.get(pk=pk)
        except Invoice.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if pk:
            data = self.get_object(pk)
            serializer = InvoiceSerializer(data)
        else:
            data =Invoice.objects.all()
            serializer = InvoiceSerializer(data, many=True)
        print(serializer.data)

        return Response(serializer.data)

    def post(self, request):
        data = request.data
        data["total_quantity"] = 0
        data["total_amount"] = 0
        serializer = InvoiceSerializer(data=data, context={'transaction_data': data['transactions']})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response()
        
        response.data = {
            'data': serializer.data
        }

        return response

    def put(self, request, pk=None):
        instance =self.get_object(pk)
        serializer = InvoiceSerializer(instance=instance,data=request.data,context={'transaction_data': request.data['transactions']}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = Response()
        response.data = {
            'data': serializer.data
        }

        return response

    def delete(self, request, pk=5):
        print("requets",request.data)
        todo_to_delete =  self.get_object(pk)

        todo_to_delete.delete()

        return Response({
            'message': 'Invoice Deleted Successfully'
        })
    

# {
#   "customer": "pta",
#   "transactions": [
#     {
#       "product": "m",
#       "price": "10.20",
#       "quantity": "1"
#     }
#   ]
# }