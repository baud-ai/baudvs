#
# Copyright 2019 The Vearch Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied. See the License for the specific language governing
# permissions and limitations under the License.

# -*- coding: UTF-8 -*-

import requests
import json
import pytest
import logging
from utils.vearch_utils import *
from utils.data_utils import *

logging.basicConfig()
logger = logging.getLogger(__name__)

__description__ = """ test case for cluster partition server """


class TestClusterPartitionServerAdd:
    def setup_class(self):
        self.logger = logger

    def test_prepare_db(self):
        response = create_db(router_url, db_name)
        logger.info(response.json())

    @pytest.mark.parametrize(
        ["embedding_size", "index_type"],
        [
            [128, "HNSW"],
            [128, "FLAT"],
            [128, "IVFPQ"],
            [128, "IVFFLAT"],
            [512, "FLAT"],
            [512, "IVFPQ"],
            [512, "IVFFLAT"],
            [512, "HNSW"],
        ],
    )
    def test_vearch_space_create(self, embedding_size, index_type):
        space_name_each = space_name + "smalldata" + str(embedding_size) + index_type
        space_config = {
            "name": space_name_each,
            "partition_num": 2,
            "replica_num": 1,
            "fields": [
                {"name": "field_int", "type": "integer"},
                {"name": "field_long", "type": "long"},
                {"name": "field_float", "type": "float"},
                {"name": "field_double", "type": "double"},
                {
                    "name": "field_string",
                    "type": "string",
                    "index": {"name": "field_string", "type": "SCALAR"},
                },
                {
                    "name": "field_vector",
                    "type": "vector",
                    "dimension": embedding_size,
                    "index": {
                        "name": "gamma",
                        "type": index_type,
                        "params": {
                            "metric_type": "InnerProduct",
                            "ncentroids": 2048,
                            "nsubvector": int(embedding_size / 4),
                            "nlinks": 32,
                            "efConstruction": 100,
                        },
                    },
                    # "format": "normalization"
                },
            ],
        }

        response = create_space(router_url, db_name, space_config)
        logger.info(response.json())

        add_embedding_size(db_name, space_name_each, 50, 100, embedding_size)

        delete_interface(
            logger,
            10,
            100,
            delete_type="by_ids",
            delete_db_name=db_name,
            delete_space_name=space_name_each,
        )


class TestClusterPartitionServerCheckSpace:
    def test_check_space(self):
        response = list_spaces(router_url, db_name)
        logger.info(response.json())
        for space in response.json()["data"]:
            assert space["doc_num"] == 4000


class TestClusterPartitionServerDestroy:
    def test_destroy_db(self):
        response = list_spaces(router_url, db_name)
        assert response.json()["code"] == 0
        for space in response.json()["data"]:
            response = drop_space(router_url, db_name, space["space_name"])
            assert response.json()["code"] == 0
        drop_db(router_url, db_name)


class TestClusterPartitionChange:
    def setup_class(self):
        self.logger = logger

    def test_prepare_db(self):
        response = create_db(router_url, db_name)
        logger.info(response.json())

    @pytest.mark.parametrize(
        ["embedding_size", "index_type"],
        [
            [128, "FLAT"],
        ],
    )
    def test_vearch_space_create(self, embedding_size, index_type):
        space_config = {
            "name": space_name,
            "partition_num": 2,
            "replica_num": 1,
            "fields": [
                {"name": "field_int", "type": "integer"},
                {"name": "field_long", "type": "long"},
                {"name": "field_float", "type": "float"},
                {"name": "field_double", "type": "double"},
                {
                    "name": "field_string",
                    "type": "string",
                    "index": {"name": "field_string", "type": "SCALAR"},
                },
                {
                    "name": "field_vector",
                    "type": "vector",
                    "dimension": embedding_size,
                    "index": {
                        "name": "gamma",
                        "type": index_type,
                        "params": {
                            "metric_type": "InnerProduct",
                            "ncentroids": 2048,
                            "nsubvector": int(embedding_size / 4),
                            "nlinks": 32,
                            "efConstruction": 100,
                        },
                    },
                    # "format": "normalization"
                },
            ],
        }

        response = create_space(router_url, db_name, space_config)
        logger.info(response.json())

        add_embedding_size(db_name, space_name, 50, 100, embedding_size)

        delete_interface(
            logger,
            10,
            100,
            delete_type="by_ids",
            delete_db_name=db_name,
            delete_space_name=space_name,
        )

    def test_check_space(self):
        response = list_spaces(router_url, db_name)
        logger.info(response.json())
        for space in response.json()["data"]:
            assert space["doc_num"] == 4000

    def test_change_partition(self):
        pids = []
        nodes = [1, 2, 3]
        response = get_space(router_url, db_name, space_name)
        target_node = 0
        nums = {}
        for partition in response.json()["data"]["partitions"]:
            nums[partition["pid"]] = partition["doc_num"]
            pids.append(partition["pid"])
            nodes.remove(partition["node_id"])
        target_node = nodes[0]
        # add partitons
        response = change_partitons(router_url, pids, target_node, 0)
        logger.info(response.json())
        assert response.json()["code"] == 0
        response = get_servers_status(router_url)
        logger.info(response.json())

        time.sleep(10)

        response = get_servers_status(router_url)
        for server in response.json()["data"]["servers"]:
            if server["server"]["name"] == target_node:
                for partition in server["partitions"]:
                    if partition["pid"] in nums:
                        assert nums[partition["pid"]] == partition["doc_num"]
                break

        # delete partitions
        response = change_partitons(router_url, pids, target_node, 1)
        logger.info(response.json())
        assert response.json()["code"] == 0
        response = get_servers_status(router_url)
        logger.info(response.json())

    def test_destroy_db(self):
        response = list_spaces(router_url, db_name)
        assert response.json()["code"] == 0
        for space in response.json()["data"]:
            response = drop_space(router_url, db_name, space["space_name"])
            assert response.json()["code"] == 0
        drop_db(router_url, db_name)
