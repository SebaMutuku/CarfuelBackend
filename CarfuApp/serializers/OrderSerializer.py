import datetime

from rest_framework import serializers
from yaml.serializer import Serializer

from CarfuApp.models import Orders, Users


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
	
	def createOrder(self, data):
		ordernumber = data['ordernumber']
		ordertime = datetime.datetime.now()
		
		orderamount = data['orderamount']
		orderlocation = data['orderlocation']
		deliverytime = data['deliverytime']
		orderdetails = data['orderdetails']
		orderstatus = data['orderstatus']
		try:
			deliveryagent = Users.objects.get(user_id=data['deliveryagent'])
			customerid = Users.objects.get(user_id=data['customerid'])
		except Users.DoesNotExist:
			return Serializer.error()
		
		order = Orders.objects.create(orderstatus=orderstatus,
		                              orderdetails=orderdetails,
		                              ordertime=ordertime, orderamount=orderamount,
		                              orderlocation=orderlocation, customerid=customerid,
		                              deliverytime=datetime.datetime.now(), ordernumber=ordernumber,
		                              deliveryagent=deliveryagent.username)
		order.save()
		print("Saved successfully ")
		return order
	
	def getAllOrders(self):
		order = Orders.objects.all()
		data = OrderSerializer(order, many=True)
		return data
