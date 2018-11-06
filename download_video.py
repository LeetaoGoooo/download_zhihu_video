# -*- encoding: utf-8 -*-

import re
import requests
import uuid
import datetime

class DownloadVideo:
    
    __slots__ = ['url', 'video_name', 'url_format', 'download_url', 'video_number', 'video_api', 'clarity_list', 'clarity']

    def __init__(self,url, clarity = 'ld', video_name=None):
        self.url = url
        self.video_name = video_name
        self.url_format = "https://www.zhihu.com/question/\d+/answer/\d+"
        self.clarity = clarity
        self.clarity_list = ['ld', 'sd', 'hd']
        self.video_api = 'https://lens.zhihu.com/api/videos'

    def check_url_format(self):
        pattern = re.compile(self.url_format)
        matches = re.match(pattern,self.url)
        if matches is None:
            raise ValueError("链接格式应符合:https://www.zhihu.com/question/{number}/answer/{number}")
        return True
    
    def get_video_number(self):
        try:
            headers = { 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
            response = requests.get(self.url, headers=headers)
            response.encoding='utf-8'
            html = response.text
            video_ids = re.findall(r'data-lens-id="(\d+)"', html)
            if video_ids:
                video_id_list = list(set([video_id for video_id in video_ids]))
                self.video_number = video_id_list[0]
                return self
            raise ValueError("获取视频编号异常:{}".format(self.url))
        except Exception as e:
            raise Exception(e)

    def get_video_url_by_number(self):
        url = "{}/{}".format(self.video_api,self.video_number)

        headers = {}
        headers['Referer'] = 'https://v.vzuu.com/video/{}'.format(self.video_number)
        headers['Origin'] = 'https://v.vzuu.com'
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
        headers['Content-Type'] = 'application/json'
        
        try:
            response = requests.get(url, headers=headers)
            response_dict = response.json()
            if self.clarity in response_dict['playlist']:
                self.download_url = response_dict['playlist'][self.clarity]['play_url']
            else:
                for clarity in self.clarity_list:
                    if clarity in response_dict['playlist']:
                        self.download_url = response_dict['playlist'][self.clarity]['play_url']
                        break
            return self
        except Exception as e:
            raise Exception(e)

    def get_video_by_video_url(self):
        response = requests.get(self.download_url)
        datetime_str = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        if self.video_name is not None:
            video_name = "{}-{}.mp4".format(self.video_name,datetime_str)
        else:
            video_name = "{}-{}.mp4".format(str(uuid.uuid1()),datetime_str)
        path = "{}".format(video_name)
        with open(path,'wb') as f:
            f.write(response.content)

    def download_video(self):
        
        if self.clarity not in self.clarity_list:
           raise ValueError("清晰度参数异常,仅支持:ld(普清),sd(标清),hd(高清)")

        if self.check_url_format():
            return self.get_video_number().get_video_url_by_number().get_video_by_video_url()

if __name__ == '__main__':
    a = DownloadVideo('https://www.zhihu.com/question/53031925/answer/524158069')
    print(a.download_video())