from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, koneksi, models, oauth2

router = APIRouter(prefix="/votes", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(koneksi.connect_db), current_user: schemas.CurrentUser = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} doesn't exist")


    query = db.query(models.Vote).filter(models.Vote.post_id ==
                                         vote.post_id, models.Vote.user_id == current_user.id)

    found_vote = query.first()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {
                                current_user.id} has already vote on post {vote.post_id}")

        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)

        db.add(new_vote)
        db.commit()

        return {"message": 'Add vote succeed'}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote doesn't exist")

        query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Delete vote succeed"}
