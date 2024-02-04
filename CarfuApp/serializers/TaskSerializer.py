from rest_framework import serializers

from CarfuApp.models import Task, TaskActivity


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("title",
                  "description",
                  "status",
                  "id",
                  "expires_on")
        model = Task

    def create(self, validated_data):
        task = Task.objects.create(expires_on=validated_data["expires_on"], description=validated_data["description"],
                                   title=validated_data["title"], status="pending")
        return task

    def update(self, validated_data, pk):
        task, created = Task.objects.update_or_create(id=pk, defaults=validated_data)
        return task, created

    @staticmethod
    def get_all_tasks():
        tasks = Task.objects.all()
        result_data = []
        for task in tasks:
            activities = TaskActivity.objects.filter(taskid=task.id)
            task_data = TaskSerializer(task).data
            task_data["activities"] = ActivitySerializer(activities, many=True).data
            result_data.append(task_data)
        return result_data


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = TaskActivity

    def create(self, validated_data):
        try:
            task = Task.objects.get(id=validated_data['taskid'])
            if task.id:
                activity = TaskActivity.objects.create(**validated_data)
                return activity
            raise serializers.ValidationError("An error occurred during TaskActivity creation")
        except Exception as e:
            print(e)
            raise serializers.ValidationError(f"Task with id {validated_data['taskid']} does not exist")

    def update(self, validated_data, pk):
        activity, created = TaskActivity.objects.update_or_create(id=pk, defaults=validated_data)
        return activity, created

    @staticmethod
    def get_all_task_activities():
        activity_data = TaskActivity.objects.all()
        data = ActivitySerializer(activity_data, many=True)
        return data
