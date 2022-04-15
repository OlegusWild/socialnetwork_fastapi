from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func

from sqlalchemy.orm import Session

from .. import models
from .. import schemas
from ..database import get_db

from .. import oauth2


router = APIRouter(
    prefix = '/posts',
    tags=['Posts']
)

@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), user_payload: dict = Depends(oauth2.get_current_user),
              limit: int=5, offset: int=0, search_string: Optional[str]=''):

    posts_query = db.query(models.Post, func.count(models.Post.id).label('votes')).\
            join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).\
                filter(models.Post.title.contains(search_string)).limit(limit).offset(offset)

    return posts_query.all()


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), user_payload: dict = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %(id)s""", {'id': id})
    # post = cursor.fetchone()

    post = db.query(models.Post, func.count(models.Post.id).label('votes')).\
            join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).\
                filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with id {id} doesn't exist...")
    
    return post


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostBase, db: Session = Depends(get_db), user_payload: dict = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # data = cursor.fetchone()

    # conn.commit()
    # return {'created post': data}

    print(user_payload)
    # create row instance
    new_post = models.Post(owner_id=user_payload.id, **post.dict())
    # add the row
    db.add(new_post)
    db.commit()
    # refresh the row taking into account its current params in db
    db.refresh(new_post)

    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user_payload: dict = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # deleted_post = cursor.fetchone()
    # if deleted_post is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with if {id} doesn't exist...")
    # print(f"The post {id} was seccessfully deleted.")
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with if {id} doesn't exist...")
    
    if post.owner_id != user_payload.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform requested action.')

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post_body: schemas.PostBase, db: Session = Depends(get_db), user_payload: dict = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %(title)s, 
    #                                    content = %(content)s, 
    #                                    published = %(published)s
    #                                    WHERE id = %(id)s RETURNING *""",
    #                                    {'title': post.title, 
    #                                    'content': post.content, 
    #                                    'published': post.published,
    #                                    'id':id})
    # updated_post = cursor.fetchone()
    # if updated_post is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with if {id} doesn't exist...")
    
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with if {id} doesn't exist...")
    
    if post.owner_id != user_payload.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform requested action.')
    
    post_query.update(post_body.dict(), synchronize_session=False)
    db.commit()

    return post