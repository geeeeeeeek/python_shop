# Create your views here.
from rest_framework.decorators import api_view, authentication_classes

from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import LoginLog
from myapp.permission.permission import isDemoAdminUser
from myapp.serializers import LoginLogSerializer


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        loginLogs = LoginLog.objects.all().order_by('-log_time')
        serializer = LoginLogSerializer(loginLogs, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['POST'])
def create(request):

    serializer = LoginLogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='创建成功', data=serializer.data)

    return APIResponse(code=1, msg='创建失败')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def update(request):
    try:
        pk = request.GET.get('id', -1)
        loginLogs = LoginLog.objects.get(pk=pk)
    except LoginLog.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    serializer = LoginLogSerializer(loginLogs, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='更新成功', data=serializer.data)

    return APIResponse(code=1, msg='更新失败')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delete(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    try:
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        LoginLog.objects.filter(id__in=ids_arr).delete()
    except LoginLog.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    return APIResponse(code=0, msg='删除成功')
