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

query3=[
  {
    "$match": {
      "publishedAt": {
        "$gte": start_date,
        "$lte": end_date
      }
    }
  },
  {
    "$group": {
      "_id": "$categoryId",
      "avgLikes": { "$avg": "$likes" },
      "avgViewCount": { "$avg": "$view_count" },
      "avgCommentCount": { "$avg": "$comment_count" }
    }
  },
  {
    "$project": {
      "_id": 1,
      "totalAvg": {
        "$avg": {
          "$add": [
            { "$multiply": ["$avgLikes", 0.33] },
            { "$multiply": ["$avgViewCount", 0.43] },
            { "$multiply": ["$avgCommentCount", 0.24] }
          ]
        }
      }
    }
  },
  {
    "$sort": {
      "totalAvg": -1
    }
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

    result = collection.aggregate(query3)


    # 결과 출력
    X_id = []
    y_totalAvg = []

    for document in result:
        print(str(document["_id"]))
        X_id.append(category[str(document["_id"])])
        y_totalAvg.append(document["totalAvg"])
        print(str(document["_id"]))
    print(X_id)
    print(y_totalAvg)
    # 막대 그래프 그리기

    plt.pie(y_totalAvg, labels=X_id, autopct='%.1f%%')
    plt.title(') 2023년3월~4월사이에 인기 있는 장르 순 조회 인기 -> 조회수, 좋아요, 댓글 수에 각각 가중치를 두어 평균을 구함 조회수 -> 0.43,좋아요 -> 0.33, 댓글 ->0.24 ')
    plt.show()
main()