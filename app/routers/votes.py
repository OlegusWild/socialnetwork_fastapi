from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import models
from .. import schemas
from ..database import get_db

from .. import utils, oauth2


router = APIRouter(
    prefix = '/votes',
    tags=['Votes']
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), user_payload: dict = Depends(oauth2.get_current_user)):
    
    if not db.query(models.Post).filter(models.Post.id == vote.post_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post {vote.post_id} not found...')

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == user_payload.id)
    vote_found = vote_query.first()
    if vote.dir == 1:
        if vote_found:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'User with id {user_payload.id} has already voted on post {vote.post_id}')

        new_vote = models.Vote(user_id=user_payload.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return {'status': 'vote seccessfully added'}
    else:
        if not vote_found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='vote doesn\'t exist yet')
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"status": "vote seccessfully deleted"}