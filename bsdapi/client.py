from time import sleep
import requests
from .auth import BsdApiAuth


class BsdApiClient(object):
    """BsdApiClient"""

    def __init__(self, base_url, api_id, api_secret):
        """Constructs the BsdApiClient

        :param base_url: The secure URL of your BSD Tools instance
        :param api_id: The Api User to make requests with
        :param api_secret: The Api Secret to make requests with
        """
        self.block_on_deferred_response = True
        self.deferred_result_max_attempts = 10
        self.deferred_poll_interval = 3

        self.base_url = base_url.rstrip('/')
        self.api_id = api_id
        self.api_secret = api_secret
        self.api_path = '/page/api/'

    def _construct_url(self, endpoint):
        """Combines the API Endpoint with the API URI base fragment

        :param endpoint: The Tools API endpoint to call. Does not need to include '/page/api'.
        :return: The complete URL path
        :rtype: string
        """
        return self.base_url + self.api_path + endpoint.strip('/')

    def _call(self, request_method, endpoint, params=None, data=None):
        """Base method for making calls through the Requests API.

        :param request_method: The Requests library method to call
        :param endpoint:
        :param params: (optional)
        :param data: (optional)
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        response = request_method(
            self._construct_url(endpoint),
            params=params,
            data=data,
            auth=BsdApiAuth(self.api_id, self.api_secret)
        )

        return self._resolve_deferred_response(response, self.deferred_result_max_attempts)

    def _resolve_deferred_response(self, response, remaining):
        """Polls the BSD API for a deferred result

        :param response:
        :param remaining:
        :return: The next deferred :class:`Response <Response>`
        :rtype: requests.Response
        """
        if remaining == 0:
            raise RuntimeError("Failed to resolve deferred response.")

        if response.status_code == 202 and self.block_on_deferred_response:
            sleep(self.deferred_poll_interval)
            return self._resolve_deferred_response(
                self.get('get_deferred_results', {'deferred_id': response.text}),
                remaining-1
            )

        return response

    def get(self, endpoint, params=None):
        """Wraps GET requests to the Blue State Digital API

        :param endpoint: The Tools API endpoint to call. Does not need to include '/page/api'.
        :param params: (optional) Dictionary or bytes to be sent in the query string for the :class:`Request`.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self._call(requests.get, endpoint, params=params)

    def post(self, endpoint, params=None, data=None):
        """Wraps POST requests to the Blue State Digital API.

        :param endpoint: The Tools API endpoint to call. Does not need to include '/page/api'.
        :param params: (optional) Dictionary or bytes to be sent in the query string for the :class:`Request`.
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self._call(requests.post, endpoint, params=params, data=data)

    def put(self, endpoint, params=None, data=None):
        """Wraps PUT requests to the Blue State Digital API.

        :param endpoint: The Tools API endpoint to call. Does not need to include '/page/api'.
        :param params: (optional) Dictionary or bytes to be sent in the query string for the :class:`Request`.
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self._call(requests.put, endpoint, params=params, data=data)

    def delete(self, endpoint, params):
        """Wraps DELETE requests to the Blue State Digital API

        :param endpoint: The Tools API endpoint to call. Does not need to include '/page/api'.
        :param params: (optional) Dictionary or bytes to be sent in the query string for the :class:`Request`.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """

        return self._call(requests.delete, endpoint, params=params)
