# Create your views here.
import datetime

from rest_framework.decorators import api_view, authentication_classes

from myapp import utils
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import Order, Thing
from myapp.permission.permission import isDemoAdminUser
from myapp.serializers import OrderSerializer


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        orders = Order.objects.all().order_by('-order_time')
        serializer = OrderSerializer(orders, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def create(request):
    """
    创建订单
    """
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

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
@authentication_classes([AdminTokenAuthtication])
def update(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    try:
        pk = request.GET.get('id', -1)
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    serializer = OrderSerializer(order, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='更新成功', data=serializer.data)
    else:
        print(serializer.errors)
        return APIResponse(code=1, msg='更新失败')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def cancel_order(request):
    """
    取消
    """
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

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

        return APIResponse(code=0, msg='取消成功', data=serializer.data)
    else:
        print(serializer.errors)
        return APIResponse(code=1, msg='更新失败')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delay(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    try:
        pk = request.GET.get('id', -1)
        order = Order.objects.get(pk=pk)
    except Order.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    if order.delayed:
        return APIResponse(code=1, msg='已超最大延期次数')
    else:
        data = {
            "delayed": True,
            "expect_time": order.expect_time + datetime.timedelta(days=30)
        }
        serializer = OrderSerializer(order, data=data)
        if serializer.is_valid():
            serializer.save()
            return APIResponse(code=0, msg='延期成功', data=serializer.data)
        else:
            print(serializer.errors)
            return APIResponse(code=1, msg='延期失败')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delete(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    try:
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        Order.objects.filter(id__in=ids_arr).delete()
    except Order.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    return APIResponse(code=0, msg='删除成功')
