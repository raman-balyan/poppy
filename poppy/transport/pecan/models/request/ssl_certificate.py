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

from poppy.model import ssl_certificate


def load_from_json(json_data):
    flavor_id = json_data.get("flavor_id")
    domain_name = json_data.get("domain_name")
    cert_type = json_data.get("cert_type")
    project_id = json_data.get("project_id")
    cert_details = json_data.get("cert_details", {})

    return ssl_certificate.SSLCertificate(flavor_id, domain_name,
                                          cert_type, project_id, cert_details)
