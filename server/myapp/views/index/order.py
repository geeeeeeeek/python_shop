# Create your views here.
import datetime

from rest_framework.decorators import api_view, authentication_classes

from myapp import utils
from myapp.auth.authentication import TokenAuthtication
from myapp.handler import APIResponse
from myapp.models import Order, Thing
from myapp.serializers import OrderSerializer


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        userId = request.GET.get('userId', -1)
        orderStatus = request.GET.get('orderStatus', '')

        orders = Order.objects.all().filter(user=userId).filter(status__contains=orderStatus).order_by('-order_time')
        serializer = OrderSerializer(orders, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def create(request):

    data = request.data.copy()
    if data['user'] is None or data['thing'] is None or data['count'] is None:
        return APIResponse(code=1, msg='参数错误')

    thing = Thing.objects.get(pk=data['thing'])
    count = data['count']
    if thing.repertory < int(count):
        return APIResponse(code=1, msg='库存不足')

    create_time = datetime.datetime.now()
    data['create_time'] = create_time
    data['order_number'] = str(utils.get_timestamp())
    data['status'] = '1'
    serializer = OrderSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        # 减库存(支付后)
        # thing.repertory = thing.repertory - int(count)
        # thing.save()

        return APIResponse(code=0, msg='创建成功', data=serializer.data)
    else:
        print(serializer.errors)
        return APIResponse(code=1, msg='创建失败')


@api_view(['POST'])
@authentication_classes([TokenAuthtication])
def cancel_order(request):
    """
    cancal
    """
    try:
        pk = request.GET.get('id', -1)
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    data = {
        'status': 7
    }
    serializer = OrderSerializer(order, data=data)
    if serializer.is_valid():
        serializer.save()
        # 加库存
        # thingId = request.data['thing']
        # thing = Thing.objects.get(pk=thingId)
        # thing.repertory = thing.repertory + 1
        # thing.save()

        # 加积分
        # order.user.score = order.user.score + 1
        # order.user.save()

        return APIResponse(code=0, msg='取消成功', data=serializer.data)
    else:
        print(serializer.errors)
        return APIResponse(code=1, msg='更新失败')
