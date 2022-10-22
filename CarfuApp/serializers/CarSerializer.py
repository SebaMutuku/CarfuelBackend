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

    def saveCar(self, data, image):
        make = data['make']
        model = data['model']
        yom = data['yom']
        mileage = data['mileage']
        price = data['price']
        car_description = data['car_description']
        color = data["color"]
        saved_on = datetime.datetime.now()
        try:
            Cars.objects.create(
                saved_on=saved_on,
                car_description=car_description,
                make=make,
                mileage=mileage,
                model=model,
                imageUrl=image,
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
        try:
            car_brands = Cars.objects.values("make", "model", "color", "yom", "car_description", "price")
            return car_brands
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def get_all_cars():
        try:
            cars = Cars.objects.all()
            if cars:
                return cars
            return None
        except Exception as e:
            print(e)
            return None
