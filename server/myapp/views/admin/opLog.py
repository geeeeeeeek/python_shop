# Create your views here.
from rest_framework.decorators import api_view

from myapp.handler import APIResponse
from myapp.models import OpLog
from myapp.serializers import OpLogSerializer


@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        opLogs = OpLog.objects.all().order_by('-re_time')[:100]
        serializer = OpLogSerializer(opLogs, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)
