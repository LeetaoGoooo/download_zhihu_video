import requests
from bs4 import BeautifulSoup


def get_video_and_answer_id_by(url:str) -> list[str]:
    answer_id = url.split("/")[-1]
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception("获取视频编号失败")
    soup = BeautifulSoup(resp.text, 'html.parser')
    video_ele = soup.find("a", class_="video-box")
    print(video_ele.attrs)
    return video_ele['data-lens-id'], answer_id


def get_video_by(video_id:str, answer_id:str) -> str:
    url = f'https://www.zhihu.com/api/v4/video/play_info?r={video_id}'
    params = {
        "content_id": answer_id,
        "content_type_str":"answer",
        "video_id":video_id,
        "scene_code":"answer_detail_web",
        "is_only_video":True}
    resp = requests.post(url, json=params)
    if resp.status_code != 200:
        raise Exception("获取视频地址失败")
    resp_json = resp.json()
    video_play = resp_json['video_play']
    playlist = video_play['playlist']["mp4"]
    return playlist[0]['url'][0]

def download_video_by(url:str, video_name:str):
    resp = requests.get(url)
    path = f"{video_name}.mp4"
    with open(path, 'wb') as f:
        f.write(resp.content)


def download_zhihu_video(url:str, name:str):
    video_id, answer_id = get_video_and_answer_id_by(url)
    print(f'video_id:{video_id}, answer_id:{answer_id}')
    video_url = get_video_by(video_id, answer_id)
    print(f'video_url:{video_url}')
    download_video_by(video_url, name)


if __name__ == '__main__':
    download_zhihu_video("https://www.zhihu.com/question/287408459/answer/502903607","测试")
