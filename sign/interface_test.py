import requests
import unittest

class GetEventListTest(unittest.TestCase):
    '''查询发布会接口测试'''

    def setUp(self):
        self.url="http://127.0.0.1:8000/api/get_event_list/"

    def test_get_evnet_null(self):
        '''发布会id为空'''

        r=requests.get(url=self.url,params={'eid':''})
        result=r.json()

        # 断言接口返回值
        try:
            self.assertEqual(result['status'],10022)
            self.assertEqual(result['message'],'query result is empty')
            print(result)
        except AssertionError as e:
            print(e.__str__())


if __name__=='__main__':
    unittest.main()