import pymongo
import json
from urllib import parse
import math
import random
from datetime import datetime
import urllib.parse
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import mplcursors
plt.rcParams['font.family'] = 'Malgun Gothic'
path='C:/Users/jmjun/OneDrive/바탕 화면/4학년 1학기/빅데이터시스템/유튜브 트렌드 프로젝트/graph_folder/'
#1)2023년 4월에 조회수가 많은 장르 순으로 조회하기
start_date = datetime(2023, 4, 1)
end_date = datetime(2023, 4, 30, 23, 59, 59, 999000)
category={
   "1": "영화 & 애니메이션",
   "2": "자동차 & 차량",
   "10": "음악",
   "15": "애완동물 & 동물",
   "17": "스포츠",
   "18": "짧은 영화",
   "19": "여행 & 이벤트",
   "20": "게임",
   "21": "비디오블로그",
   "22": "사람 & 블로그",
   "23": "코미디",
   "24": "엔터테이먼트",
   "25": "뉴스 & 정치학",
   "26": "스타일",
   "27": "교육",
   "28": "과학 & 기술",
    "29": "뉴스",
   "30": "영화",
   "31": "애니메이션",
   "32": "액션",
   "33": "클래식",
   "34": "코미디",
   "35": "다큐멘터리",
   "36": "드라마",
   "37": "가족",
   "38": "외국어",
   "39": "공포",
   "40": "공상과학",
   "41": "스릴러",
   "42": "스포츠",
   "43": "쇼",
   "44": "예고편"
}

query6=[
  {
    "$group": {
      "_id": "$title",
      "likes": {"$sum": "$likes" },
      "view_count": {"$sum": "$view_count" },
      "comment_count": {"$sum": "$comment_count"},
        "dislikes": {"$sum": "$dislikes" }
    }
  },{"$sort":{"commet_count":-1}}
]

def add_to_2d_array(arr, value1, value2,value3):
    arr.append([value1, value2, value3])

# 빈 2차원 배열 생성
two_dimensional_array = []



def main():


    host = "localhost"
    port = "27017"
    user = "test_admin"
    pwd = "admin"
    db = "admin"
    client = pymongo.MongoClient(f'mongodb://{user}:{urllib.parse.quote_plus(pwd)}@{host}:{port}/{db}')
    print(1)
    db_conn = client.get_database(db)
    collection = db_conn.get_collection("youtube")
    print(2)
    result = collection.aggregate(query6)

    print(type(result))
    # 결과 출력

    title=[]
    y_viewcount=[]
    y_likes=[]
    y_dislikes = []
    y_totalComments = []

    for document in result:
        print(document)
        title.append(str(document["_id"]))
        y_viewcount.append(document["view_count"])
        y_likes.append(document["likes"])
        y_dislikes.append(document["dislikes"])
        y_totalComments.append(document["comment_count"])
        add_to_2d_array(two_dimensional_array,str(document["_id"]), (document["likes"]), document["dislikes"])
    print(two_dimensional_array)

    # 막대 그래프 그리기

    labels = title

    fig, ax = plt.subplots()
    line, = ax.plot(y_likes, y_dislikes, "ro")
    mplcursors.cursor(ax).connect(
        "add", lambda sel: sel.annotation.set_text(labels[sel.index]))


    ax.set_xlabel('좋아요수')
    ax.set_ylabel('싫어요수')


    plt.show()





main()