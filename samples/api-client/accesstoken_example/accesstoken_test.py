# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime
import os
import sys
import time
import uuid

import pytest

# Add command receiver for bootstrapping device registry / device for testing
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "mqtt_example"))  # noqa
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "manager"))
import accesstoken  # noqa
import manager  # noqa


cloud_region = "us-central1"
device_id_template = "test-device-{}"
rsa_cert_path = "resources/rsa_cert.pem"
rsa_private_path = "resources/rsa_private.pem"  # Must match rsa_cert
topic_id = "test-device-events-{}".format(uuid.uuid4())

project_id = os.environ["GOOGLE_CLOUD_PROJECT"]
service_account_json = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]
pubsub_topic = "projects/{}/topics/{}".format(project_id, topic_id)

# This format is used in the `clean_up_registries()` below.
registry_id = "test-registry-{}-{}".format(uuid.uuid4().hex, int(time.time()))


def test_generate_gcp_jwt_token():
    device_id = device_id_template.format("RSA256")
    scope = "scope1 scope2 "
    manager.open_registry(
        service_account_json, project_id, cloud_region, pubsub_topic, registry_id
    )

    manager.create_rs256_device(
        service_account_json,
        project_id,
        cloud_region,
        registry_id,
        device_id,
        rsa_cert_path,
    )

    manager.get_device(
        service_account_json, project_id, cloud_region, registry_id, device_id
    )
    token = accesstoken.generate_gcp_token(
        project_id,
        cloud_region,
        registry_id,
        device_id,
        scope,
        "RSA256",
        rsa_private_path,
    )
    # clean up
    manager.delete_device(
        service_account_json, project_id, cloud_region, registry_id, device_id
    )

    manager.delete_registry(service_account_json, project_id, cloud_region, registry_id)
