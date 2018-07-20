from django.test import TestCase
from django.contrib.auth.models import User
from sign.models import Event,Guest


# Create your tests here.
class IndexPageTest(TestCase):
    '''
    测试index登录首页
    '''

    def test_index_page_renders_index_template(self):
        '''
        测试index视图
        :return:
        '''
        response=self.client.get('/index/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'index.html')

class LoginActionTest(TestCase):
    '''
    测试登录动作
    '''

    def setUp(self):
        User.objects.create_user('admin2','admin2@mail.com','admin1234')


    def test_add_admin(self):
        '''
        测试添加用户
        :return:
        '''

        user=User.objects.get(username="admin2")
        self.assertEqual(user.username,"admin2")
        self.assertEqual(user.email,"admin2@mail.com")


    def test_login_action_username_password_null(self):
        '''
        用户密码为空
        :return:
        '''
        test_data={'username':'','password':''}
        response=self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code,200)
        self.assertIn(b"username or password error!" ,response.content)


    def test_login_action_username_password_error(self):
        '''
        用户名密码错误
        :return:
        '''
        test_data={'username':'abc','password':'123'}
        response=self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code,200)
        self.assertIn(b'username or password error!',response.content)

    def test_login_action_success(self):
        '''
        登录成功
        :return:
        '''

        test_data={'username':'admin2','password':'admin1234'}
        response=self.client.post('/login_action/',data=test_data)
        self.assertEqual(response.status_code,302)

class EventManageTest(TestCase):
    '''发布会管理'''

    def setUp(self):
        User.objects.create_user("admin3",'admin3@mail.com','admin123456')
        Event.objects.create(name='xiaomi5',limit=2000,addresss='beijing',status=1,start_time='2017-8-10 12:30:00')
        self.login_user={'username':'admin3','password':'admin123456'}

    def test_event_manage_success(self):
        '''
        测试发布会xiaomi5
        :return:
        '''
        response=self.client.post('/login_action/',data=self.login_user)
        response=self.client.post('/event_manage/')
        self.assertEqual(response.status_code,200)
        self.assertIn(b"xiaomi5",response.content)
        self.assertIn(b"beijing",response.content)

    def test_event_manage_sreach_success(self):
        '''
        测试发布会搜索
        :return:
        '''
        response=self.client.post('/login_action/',data=self.login_user)
        response=self.client.post('/search_name/',{"name":"xiaomi5"})
        self.assertEqual(response.status_code,200)
        self.assertIn(b"xiaomi5",response.content)
        self.assertIn(b"beijing",response.content)


class GuestManageTest(TestCase):
    '''嘉宾管理'''

    def setUp(self):
        User.objects.create_user("admin4","admin4@mail.com","admin123456")
        Event.objects.create(id=1,name="xiaomi5",limit=2000,address='beijing',status=1,start_time='2017-8-10 12:30:00')
        Guest.objects.create(realname='alen',phone=18611001100,email='alen@qq.com',sign=0,event_id=1)
        self.login_user={'username':'admin4','password':'admin123456'}

    def test_event_manage_success(self):
        '''
        测试嘉宾信息
        :return:
        '''
        response=self.client.post('/login_action/',data=self.login_user)
        response=self.client.post('/guest_manage/')
        self.assertEqual(response.status_code,200)
        self.assertIn(b"alen",response.content)
        self.assertIn(b"18611001100",response.content)


    def test_guest_manage_sreach_success(self):
        '''
        测试嘉宾搜索
        :return:
        '''
        response=self.client.post('/login_action/',data=self.login_user)
        response=self.client.post('/search_phone/',{"phone":"18611001100"})
        self.assertEqual(response.status_code,200)
        self.assertIn(b"alen",response.content)
        self.assertIn(b"18611001100",response.content)


class SignIndexActionTest(TestCase):
    '''发布会签到'''
    def setUp(self):
        User.objects.create_user('admin5','admin5@mail.com','admin123456')
        Event.objects.create(id=1,name='xiaomi5',limit=2000,address='beijing',status=1,start_time='2017-8-10 12:30:00')
        Event.objects.create(id=2,name="oneplus4",limit=2000,address='shenzhen',status=1,start_time='2017-6-10 12:30:00')
        Guest.objects.create(realname='jack',phone=15611023302,email='jack@qq.com',sign=0,event_id=1)
        Guest.objects.create(realname='umsa',phone=15478952200,email='umsa@qq.com',sign=1,event_id=2)
        self.login_user={'username':'admin5','password':'admin123456'}

    def test_sign_index_action_phone_null(self):
        '''手机号为空'''
        response=self.client.post('/login_action/',data=self.login_user)
        response=self.client.post('/sign_index_action/1/',{"phone":''})
        self.assertEqual(response.status_code,200)
        self.assertIn(b"phone error.",response.content)

    def test_sign_index_phone_or_event_id_error(self):
        '''手机号或发布会id错误'''
        response=self.client.post('/login_action/',data=self.login_user)
        response=self.client.post('/sign_index_action/2/',{"phone":'41111111'})
        self.assertEqual(response.status_code,200)
        self.assertIn(b"event id or phone error.",response.content)

    def test_sign_index_action_user_sign_has(self):
        '''用户已签到'''
        response=self.client.post('/login_action/',data=self.login_user)
        response=self.client.post('/sign_index_action/2/',{"phone":'15478952200'})
        self.assertEqual(response.status_code,200)
        self.assertIn(b"user has sign in.",response.content)

    def test_sign_index_action_sign_success(self):
        '''签到成功'''
        response=self.client.post('/login_action/',data=self.login_user)
        response=self.client.post('/sign_index_action/1/',{"phone":'15611023302'})
        self.assertEqual(response.status_code,200)
        self.assertIn(b"sign in success!",response.content)



