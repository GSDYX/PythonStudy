import weibo
import json
import requests
import uploadBili


# 下载并上传至b站
def downloadAndUpload():
    userInfoList = []
    with open('user_id_list.txt', encoding='utf-8') as file_obj:
        for content in file_obj:
            contentSplit = content.split(' ')
            userInfoMap = {'userName': contentSplit[1], 'userId': contentSplit[0]}
            userInfoList.append(userInfoMap)
        file_obj.close

    for userInfo in userInfoList:
        filePath = 'C:/Develop/python/uploadBili/weibo/'
        filePath = filePath + userInfo['userName'] + \
            '/' + userInfo['userId'] + '.json'

        weiboInfoList = []
        with open(filePath, 'r', encoding='utf-8') as f:
            jsonData = json.load(f)
            weiboInfoList = jsonData['weibo']
            f.close

        for weiboInfo in weiboInfoList:
            if weiboInfo['video_url'] is None or weiboInfo['video_url'] == '':
                continue
                
            if str(datetime.date.today()) == weiboInfo['created_at']:
                continue

            file_path = 'C:/download/weiboDownload/' + weiboInfo['text'] + '.mp4'
            vedioFile = requests.get(weiboInfo['video_url'])

            with open(file_path, 'wb') as f:
                f.write(vedioFile.content)
                f.close

            title = weiboInfo['text']
            resourceUrl = 'https://weibo.com/tv/show/' + weiboInfo['object_id']

            uploadBili.upload(title,resourceUrl)


# 爬取微博信息
# weibo.main()
downloadAndUpload()
