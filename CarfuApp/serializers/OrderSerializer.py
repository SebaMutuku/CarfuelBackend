import datetime

from django.contrib.auth.models import User
from rest_framework import serializers

from CarfuApp.models import Orders


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'orderid',
            'ordernumber',
            'customerid',
            'orderamount',
            'orderlocation',
            'deliverytime',
            'orderdetails',
            'orderstatus',
            'deliveryagent'
        )
        model = Orders

    def create(self, data):
        ordernumber = data['ordernumber']
        ordertime = datetime.datetime.now()
        orderamount = data['orderamount']
        orderlocation = data['orderlocation']
        deliverytime = data['deliverytime']
        orderdetails = data['orderdetails']
        orderstatus = data['orderstatus']
        try:
            deliveryagent = User.objects.get(username=data['deliveryagent'])
            customerid = User.objects.get(pk=data['customerid'])
        except User.DoesNotExist as e:
            return e

        order = Orders.objects.create(orderstatus=orderstatus,
                                      orderdetails=orderdetails,
                                      ordertime=ordertime, orderamount=orderamount,
                                      orderlocation=orderlocation, customerid=customerid,
                                      deliverytime=datetime.datetime.now(), ordernumber=ordernumber,
                                      deliveryagent=deliveryagent.username)
        order.save()
        print("Saved successfully ")
        return order

    @staticmethod
    def get_all_orders():
        order = Orders.objects.all()
        data = OrderSerializer(order, many=True)
        return data
