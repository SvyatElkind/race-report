from flask_restful import Api as _Api


class Api(_Api):
    """Rewrite class method

    Used to create response in ether json or xml format defined in Flask error
    handler, as restful api returns response only in json format.
    """

    def error_router(self, original_handler, error):
        """Always pass API errors to original_handler.

        Args:
            original_handler: the original Flask error handler for the app
            error: the exception raised while handling the request

        Returns:
            original_handler call with exception
        """
        return original_handler(error)
