# Create your views here.
from django.db import connection
from rest_framework.decorators import api_view, authentication_classes

from myapp import utils
from myapp.handler import APIResponse
from myapp.models import Classification, Thing, Tag, User
from myapp.serializers import ThingSerializer, ClassificationSerializer, ListThingSerializer, DetailThingSerializer
from myapp.utils import dict_fetchall


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        keyword = request.GET.get("keyword", None)
        c = request.GET.get("c", None)
        tag = request.GET.get("tag", None)
        sort = request.GET.get("sort", 'recent')

        # 排序方式
        order = '-create_time'
        if sort == 'recent':
            order = '-create_time'
        elif sort == 'hot' or sort == 'recommend':
            order = '-pv'

        if keyword:
            things = Thing.objects.filter(title__contains=keyword).order_by(order)
        elif c and int(c) > -1:
            ids = [c]
            classifications = Classification.objects.filter(pid=c)
            serializer = ClassificationSerializer(classifications, many=True)
            subData = serializer.data
            for item in subData:
                # 添加二级分类的id
                ids.append(item['id'])
            print(ids)

            things = Thing.objects.filter(classification_id__in=ids).order_by(order)

        elif tag:
            tag = Tag.objects.get(id=tag)
            print(tag)
            things = tag.thing_set.all().order_by(order)
        else:
            things = Thing.objects.all().defer('wish').order_by(order)

        serializer = ListThingSerializer(things, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['GET'])
def detail(request):
    try:
        pk = request.GET.get('id', -1)
        thing = Thing.objects.get(pk=pk)
    except Thing.DoesNotExist:
        utils.log_error(request, '对象不存在')
        return APIResponse(code=1, msg='对象不存在')

    if request.method == 'GET':
        serializer = ThingSerializer(thing)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['POST'])
def increaseWishCount(request):
    try:
        pk = request.GET.get('id', -1)
        thing = Thing.objects.get(pk=pk)
        # wish_count加1
        thing.wish_count = thing.wish_count + 1
        thing.save()
    except Thing.DoesNotExist:
        utils.log_error(request, '对象不存在')
        return APIResponse(code=1, msg='对象不存在')

    serializer = ThingSerializer(thing)
    return APIResponse(code=0, msg='操作成功', data=serializer.data)

@api_view(['POST'])
def increaseRecommendCount(request):
    try:
        pk = request.GET.get('id', -1)
        thing = Thing.objects.get(pk=pk)
        # recommend_count加1
        thing.recommend_count = thing.recommend_count + 1
        thing.save()
    except Thing.DoesNotExist:
        utils.log_error(request, '对象不存在')
        return APIResponse(code=1, msg='对象不存在')

    serializer = ThingSerializer(thing)
    return APIResponse(code=0, msg='操作成功', data=serializer.data)

@api_view(['POST'])
def addWishUser(request):
    try:
        username = request.GET.get('username', None)
        thingId = request.GET.get('thingId', None)

        if username and thingId:
            user = User.objects.get(username=username)
            thing = Thing.objects.get(pk=thingId)

            if user not in thing.wish.all():
                thing.wish.add(user)
                thing.wish_count += 1
                thing.save()

    except Thing.DoesNotExist:
        utils.log_error(request, '操作失败')
        return APIResponse(code=1, msg='操作失败')

    serializer = ThingSerializer(thing)
    return APIResponse(code=0, msg='操作成功', data=serializer.data)

@api_view(['POST'])
def removeWishUser(request):
    try:
        username = request.GET.get('username', None)
        thingId = request.GET.get('thingId', None)

        if username and thingId:
            user = User.objects.get(username=username)
            thing = Thing.objects.get(pk=thingId)

            if user in thing.wish.all():
                thing.wish.remove(user)
                thing.wish_count -= 1
                thing.save()

    except Thing.DoesNotExist:
        utils.log_error(request, '操作失败')
        return APIResponse(code=1, msg='操作失败')

    return APIResponse(code=0, msg='操作成功')

@api_view(['GET'])
def getWishThingList(request):
    try:
        username = request.GET.get('username', None)
        if username:
            user = User.objects.get(username=username)
            things = user.wish_things.all()
            serializer = ListThingSerializer(things, many=True)
            return APIResponse(code=0, msg='操作成功', data=serializer.data)
        else:
            return APIResponse(code=1, msg='username不能为空')

    except Exception as e:
        utils.log_error(request, '操作失败' + str(e))
        return APIResponse(code=1, msg='获取心愿单失败')


@api_view(['POST'])
def addCollectUser(request):
    try:
        username = request.GET.get('username', None)
        thingId = request.GET.get('thingId', None)

        if username and thingId:
            user = User.objects.get(username=username)
            thing = Thing.objects.get(pk=thingId)

            if user not in thing.collect.all():
                thing.collect.add(user)
                thing.collect_count += 1
                thing.save()

    except Thing.DoesNotExist:
        utils.log_error(request, '操作失败')
        return APIResponse(code=1, msg='操作失败')

    serializer = DetailThingSerializer(thing)
    return APIResponse(code=0, msg='操作成功', data=serializer.data)


@api_view(['POST'])
def removeCollectUser(request):
    try:
        username = request.GET.get('username', None)
        thingId = request.GET.get('thingId', None)

        if username and thingId:
            user = User.objects.get(username=username)
            thing = Thing.objects.get(pk=thingId)

            if user in thing.collect.all():
                thing.collect.remove(user)
                thing.collect_count -= 1
                thing.save()

    except Thing.DoesNotExist:
        utils.log_error(request, '操作失败')
        return APIResponse(code=1, msg='操作失败')

    return APIResponse(code=0, msg='操作成功')


@api_view(['GET'])
def getCollectThingList(request):
    try:
        username = request.GET.get('username', None)
        if username:
            user = User.objects.get(username=username)
            things = user.collect_things.all()
            serializer = ListThingSerializer(things, many=True)
            return APIResponse(code=0, msg='操作成功', data=serializer.data)
        else:
            return APIResponse(code=1, msg='username不能为空')

    except Exception as e:
        utils.log_error(request, '操作失败' + str(e))
        return APIResponse(code=1, msg='获取收藏失败')


