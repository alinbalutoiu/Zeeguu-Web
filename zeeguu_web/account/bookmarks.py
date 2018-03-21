import datetime

from zeeguu_web.account.api.bookmarks import get_bookmarks_by_date
from . import account, login_first
import flask
from zeeguu.model import Bookmark, Text
import zeeguu


@account.route("/bookmarks")
@login_first
def bookmarks():

    d = datetime.datetime.now() - datetime.timedelta(days = 365)
    data = get_bookmarks_by_date(d)

    # bookmarks_list, dates = flask.g.user.bookmarks_by_date()
    #
    # most_recent_seven_days = dates[0:6]
    #
    # urls_by_date = {}
    # bookmarks_by_url = {}
    # for date in most_recent_seven_days:
    #     for bookmark in bookmarks_list[date]:
    #         urls_by_date.setdefault(date, set()).add(bookmark.text.url)
    #         bookmarks_by_url.setdefault(bookmark.text.url, []).append(bookmark)
    #
    # bookmark_counts_by_date = flask.g.user.bookmark_counts_by_date()

    return flask.render_template("bookmarks.html",
                                 bookmarks_by_url=data["bookmarks_by_url"],
                                 urls_by_date=data["urls_by_date"],
                                 sorted_dates=data["sorted_dates"],
                                 bookmark_counts_by_date=data["bookmark_counts_by_date"])
        # ,
        #                          user=flask.g.user)


# These following endpoints are invoked via ajax calls from the bookmarks page

@account.route("/delete_bookmark/<bookmark_id>", methods=("POST",))
@login_first
def delete(bookmark_id):
    # Beware, the there is another delete_bookmark in the zeeguu API!!!
    bookmark = Bookmark.query.get(bookmark_id)
    if not bookmark:
        return "Not found"

    text = Text.query.get(bookmark.text.id)

    # bookmark goes
    zeeguu.db.session.delete(bookmark)
    zeeguu.db.session.commit()

    # If no more bookmarks point to the text, text goes too
    if not (text.all_bookmarks(flask.g.user)):
        zeeguu.db.session.delete(text)
        zeeguu.db.session.commit()

    return "OK"


@account.route("/starred_bookmark/<bookmark_id>/<user_id>", methods=("POST",))
@login_first
def starred_word(bookmark_id, user_id):
    bookmark = Bookmark.query.get(bookmark_id)
    bookmark.starred = True
    zeeguu.db.session.add(bookmark)
    zeeguu.db.session.commit()
    return "OK"


@account.route("/unstarred_bookmark/<bookmark_id>/<user_id>", methods=("POST",))
@login_first
def unstarred_word(bookmark_id, user_id):
    bookmark = Bookmark.query.get(bookmark_id)
    bookmark.starred = False
    zeeguu.db.session.add(bookmark)
    zeeguu.db.session.commit()
    return "OK"
