from BiliClient import VideoUploader
import time
import requests
import json
import os
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

logging.basicConfig(filename='uploadBili.log', level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT)

def upload(title,resourceUrl):
    cookies = {  # 这里是账号登录后获得的cookie
        "SESSDATA": "ca289b68%2C1623860734%2Ce0520*c1",
        "bili_jct": "f9293696e3c878f29686de0258f170da",
    }

    video_uploader = VideoUploader(cookies, title)  # 创建一个视频发布任务，视频标题为"测试视频"
    # video_uploader = VideoUploader(cookies) #也可以这样不提供标题，后面添加视频文件时自动使用文件名做标题

    videoFileName = "C:/download/weiboDownload/" + title + ".mp4"

    try:
        upvideo = video_uploader.uploadFile(videoFileName)  # 上传本地视频E:\测试视频.mp4到B站服务器
    except:
        logging.error("上传失败："+videoFileName+" 不存在")

    video_uploader.add(upvideo)  # 添加上面上传的视频到视频发布任务，可以一次发布多个视频(分P)

    video_uploader.setCopyright(2)  # 这个视频稿件是转载的
    # video_uploader.setCopyright(1) #这个视频稿件是原创的

    # 如果是转载的，在这里添加源网址，发布后会显示在简介中，原创作品不需要
    video_uploader.setSource(resourceUrl)

    # video_uploader.setDesc(f''+videoName)  # 添加视频简介

    # print(video_uploader.getTags()) #视频上传后，官方会推荐几个视频标签，这里把他显示出来

    video_uploader.setTag(["搞笑", "生活", "日常"])  # 这里给视频设置多个标签

    time.sleep(5)  # 下面获取视频封面，先等5s让官方有时间生成封面
    pics = video_uploader.recovers(upvideo)  # 上面上传视频得到upvideo后，官方会自动提供几个封面选择作为视频封面
    # print(pics)  # pics为上面获取的官方提供的封面，这里显示出来

    while len(pics) ==0:
        pics = video_uploader.recovers(upvideo)
        time.sleep(1)

    video_uploader.setCover(pics[0])  # 将官方给的第一个封面作为视频封面，也可以提供一个url自定义封面
    
    #video_uploader.setCover(r"E:\1.jpg") #将本地图片设置为封面

    video_uploader.setTid(174)  # 设置分区编号，174为 生活，其他分区
 
    video_uploader.submit()  # 这里发布视频，发布后会审核
    logging.info("title:"+title+" resourceUrl:"+resourceUrl + " 发布成功")
    print("title:"+title+" resourceUrl:"+resourceUrl+ " 发布成功")

    time.sleep(60)
    if os.path.exists(videoFileName):
        os.remove(videoFileName)


