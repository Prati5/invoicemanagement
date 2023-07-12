from rest_framework import serializers
from .models import Invoice,Transaction
from decimal import Decimal

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields= ('id','product','quantity','price','line_total',)

        
class InvoiceSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")

    class Meta:
        model = Invoice
        fields = ('id','customer','total_amount','total_quantity','date',)

    def to_representation(self, instance):
        serialized_data = super().to_representation(instance)
        transactions = instance.invoice_transaction.all()
        transactions = TransactionSerializer(transactions, many=True)
        serialized_data['transactions'] =transactions.data
        return serialized_data
    
    def validate(self, attrs):
        transaction_data = self.context.get('transaction_data')
        customer = attrs.get('customer')
        if not customer:
            raise serializers.ValidationError("Customer can not be empty")

        if not transaction_data:
            raise serializers.ValidationError("Transaction data is required.")
        
        for transaction in transaction_data:
            product = transaction.get("product")
            quantity = transaction.get("quantity")
            price = transaction.get("price")

            if not isinstance(product, str) or not product:
                raise serializers.ValidationError("Product should be a non-empty string.")
            
            if not quantity or int(quantity) <= 0:
                raise serializers.ValidationError("Quantity should be a positive integer.")
            
            if not price or Decimal(price) <= 0:
                raise serializers.ValidationError("Price should be a positive number.")
        
        return super().validate(attrs)

    def create(self, validated_data):
        transaction_data = self.context.get('transaction_data')
        for transaction in transaction_data:
            transaction['line_total'] = Decimal(transaction['price']) * Decimal(transaction["quantity"])
            validated_data['total_amount'] = validated_data['total_amount'] + int(transaction['line_total'])
            validated_data['total_quantity'] = validated_data['total_quantity'] + int(transaction['quantity'])
        invoice_instance = super().create(validated_data)

        for transaction in transaction_data:
            transaction['line_total'] = Decimal(transaction['price']) * Decimal(transaction["quantity"])
            transaction['invoice_id'] = invoice_instance
            Transaction.objects.create(**transaction)
        return invoice_instance
    
    
    def update(self, instance, validated_data):
        transaction_data = self.context.get('transaction_data')
        validated_data['total_amount']  = 0
        validated_data['total_quantity'] = 0
        for transaction in transaction_data:
            transaction['line_total'] = Decimal(transaction['price']) * Decimal(transaction["quantity"])
            validated_data['total_amount'] = validated_data['total_amount'] + int(transaction['line_total'])
            validated_data['total_quantity'] = validated_data['total_quantity'] + int(transaction['quantity'])
            if 'id' in transaction:
                transaction_instance = instance.invoice_transaction.filter(id=transaction.get('id')).last()
                if transaction_instance:
                    transaction_instance.line_total = transaction['line_total']
                    transaction_instance.price = transaction['price']
                    transaction_instance.quantity = transaction['quantity']
                    transaction_instance.save()
            else:
            
                transaction['invoice_id'] = instance
                Transaction.objects.update_or_create(**transaction)
        instance.total_amount = validated_data['total_amount']
        instance.total_quantity = validated_data['total_quantity']
        instance.customer = validated_data["customer"]
        instance.save()
        return instance