import flask
import requests
import zeeguu

from zeeguu_web.account.api.api_exceptions import APIConnectionError


class API:

    @classmethod
    def __check_response(cls, response):
        if response.status_code is 200:
            return response
        else:
            raise APIConnectionError(response.status_code)

    @classmethod
    def api_path(cls, path):
        return zeeguu.app.config.get("ZEEGUU_API") + "/" + path

    @classmethod
    def post(cls, path, payload={}, params={}, session_needed=False, session=None):
        if session_needed:
            if session is None:
                session_id = flask.session["session_id"]
            else:
                session_id = session
            params["session"] = session_id
        try:
            resp = requests.post(cls.api_path(path), data=payload, params=params)
        except Exception:
            raise APIConnectionError(404)
        return cls.__check_response(resp)

    @classmethod
    def get(cls, path, payload={}, params={}, session_needed=False, session=None):
        if session_needed:
            if session is None:
                session_id = flask.session["session_id"]
            else:
                session_id = session
            params["session"] = session_id
        try:
            resp = requests.get(cls.api_path(path), data=payload, params=params)
        except Exception:
            raise APIConnectionError(404)
        return cls.__check_response(resp)