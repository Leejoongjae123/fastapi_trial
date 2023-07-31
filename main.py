from fastapi import FastAPI
from typing import List
from starlette.middleware.cors import CORSMiddleware
import model
from db import session
from model import PostingTable, Posting
# from mangum import Mangum
from typing import List, Optional
from sqlalchemy import or_, and_
from fastapi import FastAPI, HTTPException


app = FastAPI() #앱을 생성한다
# handler=Mangum(app) #LAMBDA 배포용 MANGUM을 가져온다.

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# ----------API 정의------------
# @app.get("/getProducts")
# def read_users():
#     users = session.query(UserTable).all()
#     return users

@app.get('/getProducts', response_model=List[Posting])
async def read_items(keyword: Optional[str] = None, platform: Optional[str] = None,page: Optional[int] = 1, sort_by: Optional[str] = None, sort_order: Optional[str] = None):
    if keyword and platform:
        print("키워드와 플랫폼이 함께 입력됨")
        # 각각의 조건을 만들어줌
        keyword_condition = PostingTable.title.contains(keyword)
        platform_condition = PostingTable.platform == platform
        # 조건들을 and_로 연결하여 모두 만족하는 레코드 검색
        postings = session.query(PostingTable).filter(and_(keyword_condition, platform_condition))
    elif keyword:
        print("키워드만 입력됨")
        keyword_condition = PostingTable.title.contains(keyword)
        postings = session.query(PostingTable).filter(keyword_condition)
    elif platform:
        print("플랫폼만 입력됨")
        platform_condition = PostingTable.platform == platform
        postings = session.query(PostingTable).filter(platform_condition)
    else:
        print("키워드와 플랫폼이 모두 입력되지 않음")
        # 모든 레코드 검색
        postings = session.query(PostingTable).all()

    # 정렬 기준에 따라 결과 소팅
    if sort_by:
        if sort_by == "dday":
            sort_column = PostingTable.dday
        elif sort_by == "demandCount":
            sort_column = PostingTable.demandCount
        elif sort_by == "applyCount":
            sort_column = PostingTable.applyCount
        else:
            sort_column = None

        if sort_column:
            if sort_order == "dsc":
                postings = postings.order_by(sort_column.desc())
            else:
                postings = postings.order_by(sort_column)


    # 페이지 당 결과 개수
    items_per_page = 20

    # 전체 결과 개수
    total_items = postings.count()

    # 페이지 번호에 따라 결과 제한
    postings = postings.offset((page - 1) * items_per_page).limit(items_per_page)

    # User 모델로 변환
    return [Posting(id=posting.id, platform=posting.platform, region=posting.region,dday=posting.dday,title=posting.title,demandCount=posting.demandCount,applyCount=posting.applyCount,imageUrl=posting.imageUrl,url=posting.url,myImage=posting.myImage) for posting in postings]


@app.post("/addProducts")
# /user?name="이름"&age=10
async def create_user(postings:List[Posting]):
    for postingData in postings:
        product = PostingTable()
        product.platform = postingData.platform
        product.region = postingData.region
        product.dday = postingData.dday
        product.title = postingData.title
        product.demandCount = postingData.demandCount
        product.applyCount = postingData.applyCount
        product.imageUrl = postingData.imageUrl
        product.url = postingData.url
        product.myImage = postingData.myImage
        session.add(product)

    session.commit()

    return {"status":'success','noPostings':len(postings)}

# @app.put("/users")
# async def update_users(users: List[User]):
#     for i in users:
#         user = session.query(UserTable).filter(UserTable.id == i.id).first()
#         user.name = i.name
#         user.price = i.price
#         user.time = i.time
#         session.commit()
#
#     return f"{users[0].name} updated..."


@app.delete("/removeProducts")
async def delete_users():
    user = session.query(PostingTable).delete()
    session.commit()
    return {'status':'remove all'}