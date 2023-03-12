from rest_framework import serializers

from myapp.models import Thing, Classification, Tag, User, Comment, Record, LoginLog, Order, OrderLog, OpLog, Banner, \
    Ad, Notice, ErrorLog, Address


class ThingSerializer(serializers.ModelSerializer):
    # 额外字段
    classification_title = serializers.ReadOnlyField(source='classification.title')

    class Meta:
        model = Thing
        fields = '__all__'

class DetailThingSerializer(serializers.ModelSerializer):
    # 额外字段
    classification_title = serializers.ReadOnlyField(source='classification.title')

    class Meta:
        model = Thing
        # 排除多对多字段
        exclude = ('wish', 'collect',)

class UpdateThingSerializer(serializers.ModelSerializer):
    # 额外字段
    classification_title = serializers.ReadOnlyField(source='classification.title')

    class Meta:
        model = Thing
        # 排除多对多字段
        exclude = ('wish', 'collect',)

class ListThingSerializer(serializers.ModelSerializer):
    # 额外字段
    classification_title = serializers.ReadOnlyField(source='classification.title')

    class Meta:
        model = Thing
        # 排除字段
        exclude = ('wish', 'collect', 'description',)


class ClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classification
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = User
        fields = '__all__'
        # exclude = ('password',)


class CommentSerializer(serializers.ModelSerializer):
    comment_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    # 额外字段
    title = serializers.ReadOnlyField(source='thing.title')
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'content', 'comment_time', 'like_count', 'thing', 'user', 'title', 'username']


class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = '__all__'


class LoginLogSerializer(serializers.ModelSerializer):
    log_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = LoginLog
        fields = '__all__'


class OpLogSerializer(serializers.ModelSerializer):
    re_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = OpLog
        fields = '__all__'


class ErrorLogSerializer(serializers.ModelSerializer):
    log_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = ErrorLog
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    expect_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    return_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    # extra
    username = serializers.ReadOnlyField(source='user.username')
    title = serializers.ReadOnlyField(source='thing.title')
    price = serializers.ReadOnlyField(source='thing.price')
    cover = serializers.FileField(source='thing.cover', required=False)

    class Meta:
        model = Order
        fields = '__all__'


class OrderLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLog
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)
    # extra
    title = serializers.ReadOnlyField(source='thing.title')

    class Meta:
        model = Banner
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = Ad
        fields = '__all__'


class NoticeSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = Notice
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False)

    class Meta:
        model = Address
        fields = '__all__'
