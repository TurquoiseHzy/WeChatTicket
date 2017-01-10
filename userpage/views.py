from codex.baseerror import *
from codex.baseview import APIView

from wechat.models import User,Activity,Ticket
import urllib


class UserBind(APIView):

    def validate_user(self):
        """
        input: self.input['student_id'] and self.input['password']
        raise: ValidateError when validating failed
        """
        url = "https://id.tsinghua.edu.cn/do/off/ui/auth/login/post/fa8077873a" \
              "7a80b1cd6b185d5a796617/0?/j_spring_security_thauth_roaming_entry"
        # 定义要提交的数据
        # url编码
        postdata = urllib.parse.urlencode({'i_user':self.input['student_id'],'i_pass':self.input['password']})
        postdata = postdata.encode('utf-8')
        # enable cookie
        try:
            res =  urllib.request.urlopen(url,postdata)
        except:
            raise ValidateError("wrong password or ")

    def get(self):
        self.check_input('openid')
        return User.get_by_openid(self.input['openid']).student_id

    def post(self):
        self.check_input('openid', 'student_id', 'password')
        user = User.get_by_openid(self.input['openid'])
        self.validate_user()
        user.student_id = self.input['student_id']
        user.save()


class ActivityDetail(APIView):

    def get(self):
        self.check_input('id')
        activity = Activity.objects.get(id = self.input['id'])
        if activity.status == 0 :
            raise ActivitystatusError("status error")
        return activity

    def post(self):
        ...

<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    def post(self):
        ...
=======
>>>>>>> parent of 9d29a54... 111
=======
>>>>>>> parent of 9d29a54... 111
=======
>>>>>>> parent of 9d29a54... 111


class TicketDetail(APIView):

    def get(self):
        self.check_input('openid','ticket')
        usr = User.objects.get(openid =  self.input['id'])
        ticket = User.objects.get(unique_id = self.input['ticket'])
        return ticket
<<<<<<< HEAD
<<<<<<< HEAD

    def post(self):
        ...


<<<<<<< HEAD
    def post(self):
        ...
=======
>>>>>>> parent of 9d29a54... 111
=======
=======
>>>>>>> parent of 9d29a54... 111

    def post(self):
        ...


<<<<<<< HEAD
>>>>>>> parent of 9d29a54... 111
=======
>>>>>>> parent of 9d29a54... 111
