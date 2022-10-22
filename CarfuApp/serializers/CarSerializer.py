import datetime

from rest_framework import serializers

from CarfuApp.models import Cars


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'make',
            'model',
            'color',
            'yom',
            'mileage',
            'sell_status',
            'price',
            'imageUrl',
            'car_description')
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
            print(e.args)
            return False

    @staticmethod
    def get_car_brands():
        car_brands = Cars.objects.values_list('make')
        return car_brands
