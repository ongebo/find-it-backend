from .user import db, User
from .lost_and_found_item import LostAndFoundItem


def get_item_as_json(item):
    reporter = User.query.filter_by(id=item.reporter_id).first()
    return {
        'id': item.id,
        'item_name': item.item_name,
        'description': item.description,
        'image_url': item.image_url,
        'report_date': item.report_date,
        'reported_by': reporter.username
    }
