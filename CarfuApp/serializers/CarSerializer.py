import datetime

from rest_framework import serializers

from CarfuApp.models import Cars


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'ordernumber',
            'customerid',
            'orderamount',
            'orderlocation',
            'deliverytime',
            'orderdetails',
            'orderstatus',
            'deliveryagent'
        )
        model = Cars

    def saveCar(self, data):
        image_url = datetime.datetime.now()
        make = data['car_make']
        model = data['car_model']
        yom = data['car_yom']
        mileage = data['car_mileage']
        price = data['car_price']
        car_description = data['car_desc']
        color = data["color"]
        saved_on = datetime.datetime.now()
        try:
            Cars.objects.create(
                saved_on=saved_on,
                car_description=car_description,
                make=make,
                mileage=mileage,
                model=model,
                image_url=image_url,
                yom=yom,
                price=price,
                color=color
            ).save()
            return True
        except Exception as e:
            e.args
            return False
