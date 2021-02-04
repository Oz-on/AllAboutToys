# Author: Oskar Domingos
# This file contains controllers for features related to CustomerRequests

from SalesFeature.interfaces import TabControllerInterface
from SalesFeature.CustomerRequests.views import CustomerRequestsTabUI, CustomerRequestDetails
from SalesFeature.CustomerRequests.models import Request


class CustomerRequestsTab(TabControllerInterface):
    def __init__(self, parent_view, database):
        self._database = database
        self._parent_view = parent_view

        # Get requests from data base
        customer_requests_raw = database.fetch_requests()
        self._customer_requests = [
            Request(
                request_id=request_raw['id'],
                request_type=request_raw['request_type'],
                username=request_raw['username'],
                user_id=request_raw['user_id'],
                content=request_raw['content'])
            for request_raw in customer_requests_raw
        ]

        self._current_subview_opened = None
        self._current_request = None

        self.__create_view()

    def __create_view(self):
        self._view = CustomerRequestsTabUI(
            parent_node=self._parent_view.center_panel,
            customer_requests=self._customer_requests,
            handle_open=self.__open_subtab,
        )
        self._parent_view.customer_req_tab = self._view

    def __open_subtab(self, request):
        self._view.close()

        self._current_request = request
        self._current_subview_opened = CustomerRequestDetails(
            parent_node=self._parent_view.center_panel,
            customer_request=self._current_request,
            handle_back=self.__handle_back,
            send_reply=self.__send_reply,
        )
        self._current_subview_opened.show()

    def __handle_back(self):
        self._current_subview_opened.close()
        self._current_subview_opened = None
        self._current_request = None
        self._view.show()

    def __send_reply(self, content):
        request_id = self._database.add_request_reply(self._current_request, content)
        # remove that request from list
        self._customer_requests = list(filter(lambda request: request.request_id != request_id, self._customer_requests))

        # Update list of requests in view
        self._view.update_previews(self._customer_requests)
        # Exit from the sub view
        self.__handle_back()

    @property
    def view(self):
        return self._view

