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
    # 키 값을 이용하여 딕셔너리 선언

    all_data = {key: [] for key in X_id}

    #리스트로 뽑기
    for sublist in two_dimensional_array:
        for item in sublist[1]:
            date_result.append(str(sublist[0])) # 데이트 리스트로 뽑기
            likes_list.append(item["likes"]) # 좋아요 리스트로 뽑기
            title_list.append(item["title"]) #제목 리스토로 뽑기
            all_data[date_result[-1]].append(item["likes"])

    print("likes_list",len(likes_list))
    print("date_result",date_result)
    date_list = list(set(date_result))
    print("date_list", date_list)
    print(all_data)
    # 2. 데이터 준비
    key_list=list(all_data.keys())
    # for key in all_data:
    #     value = all_data[key]
    #     print(f"{key}: {value}")

    for j,key in enumerate(all_data):
        globals()["data_{}".format(j)]=all_data[key]

    print(len(all_data))
    # 3. 그래프 그리기
    fig, ax = plt.subplots()
    # fig, ax2 = plt.subplots()
    # ax.boxplot([data_0], notch=True, whis=2.5)

    #ax.boxplot([data_1,data_2,data_3,data_4,data_5,data_6,data_7,data_8,data_9,data_10,data_11,data_12,data_13,data_14,data_15,data_16,data_17,data_18,data_19,data_20,data_21,data_22,data_23,data_24,data_25,data_26,data_27,data_28,data_29], notch=True, whis=2.5)
    ax.boxplot([data_0])
    #ax.set_xticklabels(['2023-04-02', '2023-04-03', '2023-04-04', '2023-04-05', '2023-04-06', '2023-04-07', '2023-04-08','2023-04-09','2023-04-10', '2023-04-11', '2023-04-12', '2023-04-13','2023-04-14','2023-04-15','2023-04-16','2023-04-17','2023-04-18','2023-04-19', '2023-04-20', '2023-04-21', '2023-04-22', '2023-04-23','2023-04-24', '2023-04-25', '2023-04-26','2023-04-27','2023-04-28','2023-04-29','2023-04-30'],rotation = 90)
    ax.set_xticklabels(['2023-04-01'])
    ax.set_ylabel('좋아요 수')

    plt.title('4월 일별 가장 높은 좋아요수를 받은 동영상 Top 10 조회하기 ')
    plt.show()

main()
