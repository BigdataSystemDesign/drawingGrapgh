import pymongo
import json
from urllib import parse
import math
import random
from datetime import datetime
import urllib.parse
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Malgun Gothic'

#1)2023년 4월에 조회수가 많은 장르 순으로 조회하기
start_date = datetime(2023, 3, 1)
end_date = datetime(2023, 3, 30, 23, 59, 59, 999000)
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

query2=[
  {
    "$match": {
      "categoryId": 24,
      "publishedAt": {
        "$gte": start_date,
        "$lte": end_date
      }
    }
  },
  {
    "$group": {
      "_id": "$channelTitle",
      "averageViewCount": {"$avg": "$view_count"}
    }
  },
  {
    "$sort": {
      "averageViewCount": -1
    }
  },
  {
    "$limit": 20
  }
]



def main():


    host = "localhost"
    port = "27017"
    user = "test_admin"
    pwd = "admin"
    db = "admin"
    client = pymongo.MongoClient(f'mongodb://{user}:{urllib.parse.quote_plus(pwd)}@{host}:{port}/{db}')

    db_conn = client.get_database(db)
    collection = db_conn.get_collection("youtube")

    result = collection.aggregate(query2)

    print(type(result))
    # 결과 출력
    X_id = []
    y_averageViewCount = []

    for document in result:

        X_id.append(str(document["_id"]))
        y_averageViewCount.append(document["averageViewCount"])
        print(str(document["_id"]))
    print(X_id)
    print(y_averageViewCount)
    # 막대 그래프 그리기
    plt.bar(X_id, y_averageViewCount)
    plt.xlabel('채널명')
    plt.ylabel('평균조회수')
    plt.xticks(X_id)
    plt.xticks(rotation=90)
    plt.title('장르가 24(엔터테인먼트)인 채널 중 2023년 3월1일부터 2023년 3월 31일까지 올라온 영상의 조회수 평균이 높은 순으로 20개 채널 조회')
    plt.show()
main()