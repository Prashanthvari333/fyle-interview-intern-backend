from flask import Response, jsonify, make_response

class APIResponse(Response):
    @classmethod
    def respond(cls, data, status_code=200):
        """
        Returns a JSON response with the given data and status code.

        :param data: The data to be included in the response.
        :param status_code: The HTTP status code for the response.
        :return: A Flask response object.
        """
        return make_response(jsonify(data=data), status_code)