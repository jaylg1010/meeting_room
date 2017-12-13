from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from meeting import models
import datetime
import json

# Create your views here.


def login(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=models.UserInfo.objects.filter(username=username, password=password).first()
        if user:
            request.session['user_info']={'user_id':user.id,'username':username}
            return redirect("/index/")
    return render(request,"login.html")


def index(request):
    '''
    获得预定的会议室，显示界面，并且插入日历，以及等待的界面
    :param request:
    :return:
    '''
    # 获取所有的会议室列表
    time_choices=models.Booking.time_choices
    return render(request,'index.html',{'time_choices':time_choices})


def booking(request):
    if request.method == "GET":
        # curr_date=datetime.datetime.now().date()
        # models.Booking.objects.create(booking_date=curr_date,booking_time=5,room_id=1,user_id=1)
        # models.Booking.objects.create(booking_date=curr_date,booking_time=7,room_id=1,user_id=2)


        room_list=models.MeetingRoom.objects.all()
        response={'status':True,'data':None,'error':None}
        try:
            # 获取预定信息
            current_date=datetime.datetime.now().date()
            choice_date=request.GET.get('choice_date')
            choice_date=datetime.datetime.strptime(choice_date,"%Y-%m-%d").date()
            if choice_date < current_date:
                raise Exception('日期小于当天')
            # print(models.Booking.objects.all().first().booking_date)
            booking_list=models.Booking.objects.filter(booking_date=choice_date)

            booking_dict={}
            for item in booking_list:
                if item.room_id not in booking_dict:
                    booking_dict[item.room_id]={item.booking_time:{'username':item.user.username,'user_id':item.user.id}}
                else:
                    booking_dict[item.room_id][item.booking_time]={'username':item.user.username,'user_id':item.user.id}

            '''
            选择的日期下的已经预定的会议室列表
            booking_dict={1(会议室ID): {5(时间段ID): {'username': 'jay'(预定的用户名), 'user_id': 1}, 7: {'username': 'jams', 'user_id': 2}}}
            '''
            # print("booking_list_+_+_+_+_+_+_+_+_+_+_+",booking_list)
            # print('booking_dict_+_+_+_+_+_+_+_+_+_+_+',booking_dict)
            data = []
            '''
            用列表再遍历的原因是要在数据中加一些前端要用到的属性,直接用ajax生成行列
            '''
            for room in room_list:
                tr = []
                tr.append({'text': room.title, 'attrs': {}})
                for time in models.Booking.time_choices:
                    '''
                    遍历所有的预定会议室的信息的时间段
                    (1,"8:00"),
                    (2,"9:00"),
                    ...
                 '''
                    if room.id in booking_dict and time[0] in booking_dict[room.id]:
                        user_info=booking_dict[room.id][time[0]]
                        if user_info['user_id'] == request.session['user_info']['user_id']:
                            td = {'text': booking_dict[room.id][time[0]]['username'], 'attrs': {'room_id': room.id, 'time_id': time[0],'class':'chosen'}}
                        else:
                            td = {'text': booking_dict[room.id][time[0]]['username'],'attrs': {'room_id': room.id, 'time_id': time[0], 'class': 'chosen','fuck':'true'}}
                    else:
                        td = {'text': '', 'attrs': {'room_id': room.id, 'time_id': time[0]}}
                    tr.append(td)
                data.append(tr)
            response['status']=True

            '''
            data=[
                    [{'text': '桃花岛', 'attrs': {}},
                     {'text': '', 'attrs': {'room_id': 1, 'time_id': 1}},
                     {'text': '', 'attrs': {'room_id': 1, 'time_id': 2}},
                     {'text': '', 'attrs': {'room_id': 1, 'time_id': 3}},
                     {'text': '', 'attrs': {'room_id': 1, 'time_id': 4}},
                     {'text': 'jay', 'attrs': {'room_id': 1, 'time_id': 5, 'class': 'chosen'}},
                     {'text': '', 'attrs': {'room_id': 1, 'time_id': 6}},
                     {'text': 'jams', 'attrs': {'room_id': 1, 'time_id': 7, 'class': 'chosen'}},
                     {'text': '', 'attrs': {'room_id': 1, 'time_id': 8}},
                     {'text': '', 'attrs': {'room_id': 1, 'time_id': 9}},
                     {'text': '', 'attrs': {'room_id': 1, 'time_id': 10}},
                     {'text': '', 'attrs': {'room_id': 1, 'time_id': 11}},
                     {'text': '', 'attrs': {'room_id': 1, 'time_id': 12}},
                     {'text': '', 'attrs': {'room_id': 1, 'time_id': 13}}],
                    [{'text': '西上官', 'attrs': {}}, {'text': '', 'attrs': {'room_id': 2, 'time_id': 1}}, {'text': '', 'attrs': {'room_id': 2, 'time_id': 2}}, {'text': '', 'attrs': {'room_id': 2, 'time_id': 3}}, {'text': '', 'attrs': {'room_id': 2, 'time_id': 4}}, {'text': '', 'attrs': {'room_id': 2, 'time_id': 5}}, {'text': '', 'attrs': {'room_id': 2, 'time_id': 6}}, {'text': '', 'attrs': {'room_id': 2, 'time_id': 7}}, {'text': '', 'attrs': {'room_id': 2, 'time_id': 8}}, {'text': '', 'attrs': {'room_id': 2, 'time_id': 9}}, {'text': '', 'attrs': {'room_id': 2, 'time_id': 10}}, {'text': '', 'attrs': {'room_id': 2, 'time_id': 11}}, {'text': '', 'attrs': {'room_id': 2, 'time_id': 12}}, {'text': '', 'attrs': {'room_id': 2, 'time_id': 13}}],
                    [{'text': '高显', 'attrs': {}}, {'text': '', 'attrs': {'room_id': 3, 'time_id': 1}}, {'text': '', 'attrs': {'room_id': 3, 'time_id': 2}}, {'text': '', 'attrs': {'room_id': 3, 'time_id': 3}}, {'text': '', 'attrs': {'room_id': 3, 'time_id': 4}}, {'text': '', 'attrs': {'room_id': 3, 'time_id': 5}}, {'text': '', 'attrs': {'room_id': 3, 'time_id': 6}}, {'text': '', 'attrs': {'room_id': 3, 'time_id': 7}}, {'text': '', 'attrs': {'room_id': 3, 'time_id': 8}}, {'text': '', 'attrs': {'room_id': 3, 'time_id': 9}}, {'text': '', 'attrs': {'room_id': 3, 'time_id': 10}}, {'text': '', 'attrs': {'room_id': 3, 'time_id': 11}}, {'text': '', 'attrs': {'room_id': 3, 'time_id': 12}}, {'text': '', 'attrs': {'room_id': 3, 'time_id': 13}}],
                    [{'text': '曲沃', 'attrs': {}}, {'text': '', 'attrs': {'room_id': 4, 'time_id': 1}}, {'text': '', 'attrs': {'room_id': 4, 'time_id': 2}}, {'text': '', 'attrs': {'room_id': 4, 'time_id': 3}}, {'text': '', 'attrs': {'room_id': 4, 'time_id': 4}}, {'text': '', 'attrs': {'room_id': 4, 'time_id': 5}}, {'text': '', 'attrs': {'room_id': 4, 'time_id': 6}}, {'text': '', 'attrs': {'room_id': 4, 'time_id': 7}}, {'text': '', 'attrs': {'room_id': 4, 'time_id': 8}}, {'text': '', 'attrs': {'room_id': 4, 'time_id': 9}}, {'text': '', 'attrs': {'room_id': 4, 'time_id': 10}}, {'text': '', 'attrs': {'room_id': 4, 'time_id': 11}}, {'text': '', 'attrs': {'room_id': 4, 'time_id': 12}}, {'text': '', 'attrs': {'room_id': 4, 'time_id': 13}}]
                ]
            '''
            print('data_+_+_+_+_+_+_+_+',data)
            response['data']=data
        except Exception as e:
            response['status'] = False
            response['error']=str(e)

        return JsonResponse(response)
    else:
        response = {'status': True, 'data': None, 'error': None}
        try:
            current_date = datetime.datetime.now().date()
            choice_date = request.POST.get('date')
            print("choice_date_+_+_+_+_+_+_+_+_+_+",choice_date,type(choice_date))
            choice_date = datetime.datetime.strptime(choice_date, "%Y-%m-%d").date()
            print(456)
            if choice_date < current_date:
                raise Exception('日期小于当天')

            post_data=json.loads(request.POST.get('data'))
            print('post_data_+_+_+_+_+_+',post_data)
            '''
            {'DEL': {}, 'ADD': {'1'(会议室ID): ['9'(时间段ID), '10']}}
          '''
            for room_id,time_list in post_data['DEL'].items():
                # 判断是否删除的会议室ID也在增加中，如果在去掉
                if room_id not in post_data['ADD']:
                    continue
                for time_id in list(time_list):
                    if time_id in post_data['ADD'][room_id]:
                        post_data['ADD'][room_id].remove(time_id)
                        post_data['DEL'][room_id].remove(time_id)

            # 增加预定会议室
            book_obj_list=[]
            for room_id,time_list in post_data['ADD'].items():
                for time_id in time_list:
                    obj = models.Booking(user_id=request.session['user_info']['user_id'],room_id=room_id,booking_date=choice_date,booking_time=time_id)
                    book_obj_list.append(obj)
            models.Booking.objects.bulk_create(book_obj_list)

            # 删除会议室预定
            from django.db.models import Q
            remove_booking = Q()
            for room_id,time_id_list in post_data['DEL'].items():
                for time_id in time_id_list:
                    temp = Q()
                    temp.connector = 'AND'
                    temp.children.append(('user_id', request.session['user_info']['user_id'],))
                    temp.children.append(('booking_date', choice_date))
                    temp.children.append(('room_id', room_id,))
                    temp.children.append(('booking_time', time_id,))

                    remove_booking.add(temp, 'OR')
            if remove_booking:
                models.Booking.objects.filter(remove_booking).delete()
        except Exception as e:
            response['status'] = False
            response['error'] = str(e)
        return JsonResponse(response)
