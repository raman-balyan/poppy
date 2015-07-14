# Copyright (c) 2014 Rackspace, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json

import pecan
from pecan import hooks

from poppy.transport.pecan.controllers import base
from poppy.transport.pecan import hooks as poppy_hooks
from poppy.transport.validators import helpers
from poppy.transport.validators.schemas import service_action
from poppy.transport.validators.stoplight import decorators
from poppy.transport.validators.stoplight import helpers as stoplight_helpers
from poppy.transport.validators.stoplight import rule


class OperatorServiceActionController(base.Controller, hooks.HookController):

    __hooks__ = [poppy_hooks.Context(), poppy_hooks.Error()]

    def __init__(self, driver):
        super(OperatorServiceActionController, self).__init__(driver)

    @pecan.expose('json')
    @decorators.validate(
        request=rule.Rule(
            helpers.json_matches_service_schema(
                service_action.ServiceActionSchema.get_schema(
                    "service_action", "POST")),
            helpers.abort_with_message,
            stoplight_helpers.pecan_getter))
    def post(self):

        service_state_json = json.loads(pecan.request.body.decode('utf-8'))
        service_action = service_state_json.get('action', None)
        project_id = service_state_json.get('project_id', None)

        services_controller = self._driver.manager.services_controller

        try:
            services_controller.services_action(project_id, service_action)
        except Exception as e:
            pecan.abort(404, detail=(
                        'Services action {0} on tenant: {1} failed, '
                        'Reason: {2}'.format(service_action,
                                             project_id, str(e))))

        return pecan.Response(None, 202)


class AdminServiceController(base.Controller, hooks.HookController):
    def __init__(self, driver):
        super(AdminServiceController, self).__init__(driver)
        self.__class__.action = OperatorServiceActionController(driver)


class AdminController(base.Controller, hooks.HookController):
    def __init__(self, driver):
        super(AdminController, self).__init__(driver)
        self.__class__.services = AdminServiceController(driver)