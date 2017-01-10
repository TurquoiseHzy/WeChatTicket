from django.shortcuts import render
from codex.baseerror import *
from codex.baseview import APIView
from django.contrib import auth
from wechat.models import Activity
# Create your views here.
class AdminLogin(APIView):

    def get(self):
        if self.request.user.is_authenticated():
            return {'code': 1 }
        else :
            return {'code': 0 }

    def post(self):
        self.check_input('password','username')
        username = self.input['username']
        password = self.input['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active :
            auth.login(self.request,user)
            return {'code' : 0}
        else:
            return {'code' : 0}

class AdminLogout(APIView):

    def post(self):
        if self.request.user is not None and self.request.user.is_authenticated():
            return {'code' : 0}
        else:
            return {'code' : 1}


class ActivityList(APIView):

    def get(self):
        if self.request.user.is_authenticated():
            return Activity.objects.all()
        else :
            return { }


class ActivityDelete(APIView):

    def post(self):
        self.check_input('id')
        aid = self.input['id']
        activity = Activity.objects.get(id = aid)
        if activity is None:
            return {'code': 1}
        else :
            activity.delete()
            return {'code': 0}


<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
class ActivityDelete(APIView):
    def post(self):
        deleteId = self.input['id']
        Activity.objects.get(id = deleteId).delete()

class ActivityCreate(APIView):
    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("User not logged in")
        newActivity = Activity.objects.create(
            name = self.input['name'],
            key = self.input['key'],
            place = self.input['place'],
            description = self.input['description'],
            pic_url = self.input['picUrl'],
            start_time = self.input['startTime'],
            end_time = self.input['endTime'],
            book_start = self.input['bookStart'],
            book_end = self.input['bookEnd'],
            total_tickets = self.input['totalTickets'],
            status = self.input['status'],
            remain_tickets = self.input['totalTickets'])
        newActivity.save()
        return newActivity.id

class ActivityDetail(APIView):
    def get(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("User not logged in")
        try:
            p = Activity.objects.get(id = self.input['id'])
            return {"name": p.name,
                    "key": p.key,
                    "description": p.description,
                    "startTime": time.mktime(p.start_time.timetuple()),
                    "endTime": time.mktime(p.end_time.timetuple()),
                    "place": p.place,
                    "bookStart": time.mktime(p.book_start.timetuple()),
                    "bookEnd": time.mktime(p.book_end.timetuple()),
                    "totalTickets": p.total_tickets,
                    "picUrl": p.pic_url,
                    "usedTickets": p.total_tickets - p.remain_tickets,
                    "bookedTickets": p.total_tickets - p.remain_tickets,
                    "currentTime": time.mktime(datetime.datetime.now().timetuple()),
                    "status": p.status}
        except:
            raise LogicError("Activity not found")

    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("User not logged in")
        try:
            p = Activity.objects.get(id = self.input["id"])
            p.name = self.input['name']
            p.place = self.input['place']
            p.description = self.input['description']
            p.pic_url = self.input['picUrl']
            p.start_time = self.input['startTime']
            p.end_time = self.input['endTime']
            p.book_start = self.input['bookStart']
            p.book_end = self.input['bookEnd']
            p.total_tickets = self.input['totalTickets']
            p.status = self.input['status']
            p.save()
            return 0
        except:
            raise LogicError("Modify Fail")

class ImageUpload(APIView):
    def post(self):
        ...

class ActivityMenu(APIView):
    def get(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("User not logged in")
        try:
            lib = WeChatLib(settings.WECHAT_TOKEN, settings.WECHAT_APPID, settings.WECHAT_SECRET)
            menu = lib.get_wechat_menu()[1]
            activityList = []
            for i in Activity.objects.all():
                index = 0
                for menu_id, j in enumerate(menu['sub_button']):
                    if j['name'] == i.name:
                        index = menu_id + 1
                activityList.append({
                    "id": i.id,
                    "name": i.name,
                    "menuIndex": index
                })
            return activityList
        except:
            raise LogicError("Get Menu Failed")

    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("User not logged in")
        try:
            activities = []
            menu = CustomWeChatView.lib.get_wechat_menu()
            menu_list = []
            for i in self.input:
                activity = Activity.objects.get(id = i)
                activities.append(activity)
                menu_list.append({"name": activity.name, "type": "click", "sub_button": [], "key": "BOOKING_ACTIVITY_" + str(Activity.objects.get(id = i).id)})
            menu[1] = {'name': '抢票', 'type': 'click', 'sub_button': menu_list, 'key': 'BOOKING_EMPTY'}
            data = {"button": menu}
            CustomWeChatView.lib.set_wechat_menu(data)
            CustomWeChatView.update_book_button(activities)
        except:
            raise LogicError("Get Menu Failed")



class ActivityCheckin(APIView):
    def get(self):
        try:
            p = Activity.objects.get(id = self.input['id'])
            return {"name": p.name,
                    "key": p.key,
                    "description": p.description,
                    "startTime": time.mktime(p.start_time.timetuple()),
                    "endTime": time.mktime(p.end_time.timetuple()),
                    "place": p.place,
                    "bookStart": time.mktime(p.book_start.timetuple()),
                    "bookEnd": time.mktime(p.book_end.timetuple()),
                    "totalTickets": p.total_tickets,
                    "picUrl": p.pic_url,
                    "usedTickets": p.total_tickets - p.remain_tickets,
                    "bookedTickets": p.total_tickets - p.remain_tickets,
                    "currentTime": time.mktime(datetime.datetime.now().timetuple()),
                    "status": p.status}
        except:
            raise LogicError("Activity not found")

    def post(self):
        if not self.request.user.is_authenticated():
            raise ValidateError("User not logged in")
        try:
            actId = self.input['actId']
            ticket = -1
            studentId = -1
            if 'studentId' in self.input:
                studentId = self.input['studentId']
            else:
                ticket = self.input['ticket']
            if ticket == -1:
                tickets = Ticket.objects.filter(student_id = studentId)
            else:
                tickets = Ticket.objects.filter(unique_id = ticket)
            for i in tickets:
                if int(i.activity.id) == int(actId):
                    i.status = 2
                    i.save()
                    return {
                        'ticket': i.unique_id,
                        'studentId': i.student_id
                    }
            raise LogicError("Check in failed")
        except:
            raise LogicError("Check in failed")
=======
>>>>>>> parent of 9d29a54... 111
=======
>>>>>>> parent of 9d29a54... 111
=======
>>>>>>> parent of 9d29a54... 111
