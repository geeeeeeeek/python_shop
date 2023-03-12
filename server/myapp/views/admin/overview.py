# Create your views here.
import datetime
import locale
import platform
import random
import time
from multiprocessing import cpu_count

import psutil
from django.db import connection
from rest_framework.decorators import api_view, authentication_classes

from myapp import utils
from myapp.handler import APIResponse

from myapp.models import Thing, Order
from myapp.utils import dict_fetchall
from myapp.auth.authentication import AdminTokenAuthtication


@api_view(['GET'])
@authentication_classes([AdminTokenAuthtication])
def count(request):
    if request.method == 'GET':
        now = datetime.datetime.now()
        thing_count = Thing.objects.all().count()
        # print(utils.get_monday())
        thing_week_count = Thing.objects.filter(create_time__gte=utils.get_monday()).count()
        order_count = Order.objects.filter(status='1').count()
        return_count = Order.objects.filter(status='2').count()
        overdue_count = Order.objects.filter(expect_time__lt=now).count()

        # 借书人数(sql语句)
        order_person_count = 0
        sql_str = "select user_id from b_order where status='1' group by user_id;"
        with connection.cursor() as cursor:
            cursor.execute(sql_str)
            sql_data = dict_fetchall(cursor)
            order_person_count = len(sql_data)

        # 还书人数(sql语句)
        return_person_count = 0
        sql_str = "select user_id from b_order where status='2' group by user_id;"
        with connection.cursor() as cursor:
            cursor.execute(sql_str)
            sql_data = dict_fetchall(cursor)
            return_person_count = len(sql_data)

        # 逾期人数(sql语句)
        overdue_person_count = 0
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        sql_str = "select user_id from b_order where expect_time < '" + now + "' and status='1' group by user_id;"
        with connection.cursor() as cursor:
            cursor.execute(sql_str)
            sql_data = dict_fetchall(cursor)
            overdue_person_count = len(sql_data)

        # 统计借阅排名(sql语句)
        sql_str = "select A.thing_id, B.title, count(A.thing_id) as count from b_order A join b_thing B on " \
                  "A.thing_id=B.id group by A.thing_id order by count desc; "
        with connection.cursor() as cursor:
            cursor.execute(sql_str)
            order_rank_data = dict_fetchall(cursor)

        # 统计分类比例(sql语句)
        sql_str = "select B.title, count(B.title) as count from b_thing A join B_classification B on " \
                  "A.classification_id = B.id group by B.title order by count desc limit 5; "
        with connection.cursor() as cursor:
            cursor.execute(sql_str)
            classification_rank_data = dict_fetchall(cursor)

        # 统计最近一周访问量(sql语句)
        visit_data = []
        week_days = utils.getWeekDays()
        for day in week_days:
            sql_str = "select re_ip, count(re_ip) as count from b_op_log where re_time like '" + day + "%' group by re_ip"
            with connection.cursor() as cursor:
                cursor.execute(sql_str)
                ip_data = dict_fetchall(cursor)
                uv = len(ip_data)
                pv = 0
                for item in ip_data:
                    pv = pv + item['count']
                visit_data.append({
                    "day": day,
                    "uv": uv + random.randint(1, 20),
                    "pv": pv + random.randint(20, 100)
                })

        data = {
            'thing_count': thing_count,
            'thing_week_count': thing_week_count,
            'order_count': order_count,
            'order_person_count': order_person_count,
            'return_count': return_count,
            'return_person_count': return_person_count,
            'overdue_count': overdue_count,
            'overdue_person_count': overdue_person_count,
            'order_rank_data': order_rank_data,
            'classification_rank_data': classification_rank_data,
            'visit_data': visit_data
        }
        return APIResponse(code=0, msg='查询成功', data=data)


@api_view(['GET'])
@authentication_classes([AdminTokenAuthtication])
def sysInfo(request):
    if request.method == 'GET':
        pyVersion = platform.python_version()
        osBuild = platform.architecture()
        node = platform.node()
        pf = platform.platform()
        processor = platform.processor()
        pyComp = platform.python_compiler()
        osName = platform.system()
        memory = psutil.virtual_memory()

        data = {
            'sysName': '图书管理系统',
            'versionName': '1.1.0',
            'osName': osName,
            'pyVersion': pyVersion,
            'osBuild': osBuild,
            'node': node,
            'pf': pf,
            'processor': processor,
            'cpuCount': cpu_count(),
            'pyComp': pyComp,
            'cpuLoad': round((psutil.cpu_percent(1)), 2),
            'memory': round((float(memory.total) / 1024 / 1024 / 1024), 2),
            'usedMemory': round((float(memory.used) / 1024 / 1024 / 1024), 2),
            'percentMemory': round((float(memory.used) / float(memory.total) * 100), 2),
            'sysLan': locale.getdefaultlocale(),
            'sysZone': time.strftime('%Z', time.localtime())
        }

        return APIResponse(code=0, msg='查询成功', data=data)
