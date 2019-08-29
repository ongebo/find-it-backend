from .. import db
from datetime import datetime


class LostAndFoundItem(db.Model):
    __tablename__ = 'lost_and_found_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    image_path = db.Column(db.String)
    report_date = db.Column(
        db.DateTime,
        nullable=False, default=datetime.utcnow()
    )
    reporter_id = db.Column('reporter_id', db.ForeignKey('users.id'))
