# Create your views here.
import datetime

from rest_framework.decorators import api_view, authentication_classes

from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import Borrow, Thing
from myapp.permission.permission import isDemoAdminUser
from myapp.serializers import BorrowSerializer


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        borrows = Borrow.objects.all().order_by('-borrow_time')
        serializer = BorrowSerializer(borrows, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def create(request):
    """
    创建借书
    """
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    data = request.data.copy()
    thing = Thing.objects.get(pk=data['thing'])
    if thing.repertory <= 0:
        return APIResponse(code=1, msg='库存不足')

    borrows = Borrow.objects.filter(thing=data['thing']).filter(user=data['user']).filter(status='1')
    if len(borrows) > 0:
        return APIResponse(code=1, msg='您已经借过该书了')

    create_time = datetime.datetime.now()
    data['create_time'] = create_time
    data['expect_time'] = create_time + datetime.timedelta(days=60)
    serializer = BorrowSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        # 减库存
        thing.repertory = thing.repertory - 1
        thing.save()

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
        borrow = Borrow.objects.get(pk=pk)
    except Borrow.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    serializer = BorrowSerializer(borrow, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='更新成功', data=serializer.data)
    else:
        print(serializer.errors)
        return APIResponse(code=1, msg='更新失败')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def return_thing(request):
    """
    还书
    """
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    try:
        pk = request.GET.get('id', -1)
        borrow = Borrow.objects.get(pk=pk)
    except Borrow.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    data = {
        'status': 2
    }
    serializer = BorrowSerializer(borrow, data=data)
    if serializer.is_valid():
        serializer.save()
        # 加库存
        thing = Thing.objects.get(pk=request.data['thing'])
        thing.repertory = thing.repertory + 1
        thing.save()

        return APIResponse(code=0, msg='借书成功', data=serializer.data)
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
        borrow = Borrow.objects.get(pk=pk)
    except Borrow.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    if borrow.delayed:
        return APIResponse(code=1, msg='已超最大延期次数')
    else:
        data = {
            "delayed": True,
            "expect_time": borrow.expect_time + datetime.timedelta(days=30)
        }
        serializer = BorrowSerializer(borrow, data=data)
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
        Borrow.objects.filter(id__in=ids_arr).delete()
    except Borrow.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    return APIResponse(code=0, msg='删除成功')
