from app.models import db, User, LostAndFoundItem


def clean_database():
    for user in User.query.all():
        db.session.delete(user)
    for item in LostAndFoundItem.query.all():
        db.session.delete(item)
    db.session.commit()
