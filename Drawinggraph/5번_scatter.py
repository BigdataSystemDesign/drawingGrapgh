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

query5=[
  {
    "$match": {
      "categoryId": 24,
      "publishedAt": {
        "$gte": start_date,
        "$lt": end_date
      }
    }
  },
  {
    "$sort": { "publishedAt": 1, "likes": -1 }
  },
  {
    "$group": {
      "_id": {
        "$dateToString": { "format": "%Y-%m-%d", "date": "$publishedAt" }
      },
      "videos": {
        "$push": {
          "title": "$title",
          "likes": "$likes"
        }
      }
    }
  },
  {
    "$project": {
      "_id": 0,
      "date": "$_id",
      "videos": { "$slice": ["$videos", 100] }
    }
  }, {
    "$sort": { "date": 1 }
  },
]

def add_to_2d_array(arr, value1, value2):
    arr.append([value1, value2])

# 빈 2차원 배열 생성
two_dimensional_array = []

def main():
    host = "localhost"
    port = "27017"
    user = "test_admin"
    pwd = "admin"
    db = "admin"
    client = pymongo.MongoClient(f'mongodb://{user}:{urllib.parse.quote_plus(pwd)}@{host}:{port}/{db}')

    db_conn = client.get_database(db)
    collection = db_conn.get_collection("youtube")

    result = collection.aggregate(query5)

    # 결과 출력
    X_id = []
    y_likes = []
    date_result=[]
    likes_list=[]
    title_list=[]
    #이차원 리스트로 정렬
    for document in result:
        y_likes.append(document["videos"])
        X_id.append((document["date"]))
        # 값을 동시에 2차원 배열에 추가
        add_to_2d_array(two_dimensional_array,(document["date"]), document["videos"])
    # print(y_likes[0][0])
    print(two_dimensional_array)
    #리스트로 뽑기
    for sublist in two_dimensional_array:
        for item in sublist[1]:
            date_result.append(sublist[0]) # 데이트 리스트로 뽑기
            likes_list.append(item["likes"]) # 좋아요 리스트로 뽑기
            title_list.append(item["title"]) #제목 리스토로 뽑기


    labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    print("likes_list",len(likes_list))
    print("date_result",len(date_result))
    # 산점도 그래프 그리기
    fig, ax = plt.subplots()
    ax.scatter(date_result, likes_list)
    # 각 점에 라벨 달기
    # for i, label in enumerate(title_list):
    #     plt.annotate(label, (date_result[i], likes_list[i]), textcoords="offset points", xytext=(0, 10), ha='center')
    # mplcursors로 마우스 이벤트 처리
    # cursors = mplcursors.cursor(scatter, hover=True)
    plt.xlabel('날짜')
    plt.ylabel('좋아요 수')
    plt.xticks(X_id)
    plt.xticks(rotation=90)
    plt.title('4월 일별 가장 높은 좋아요수를 받은 동영상 Top 10 조회하기')
    plt.show()

main()
