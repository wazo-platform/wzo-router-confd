# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Optional

from urllib.parse import urlparse
from uuid import uuid4
from typing import Tuple

from consul import Consul  # type: ignore
from fastapi import FastAPI
from pydantic import NoneBytes


class ConsulService(object):
    def __init__(self, consul_uri: str):
        uri = urlparse(consul_uri)
        self._consul_uri = consul_uri
        self._consul = Consul(host=uri.hostname, port=uri.port)

    def register(
        self,
        service_id: str,
        name: str,
        address: Optional[str] = None,
        port: Optional[int] = None,
        tags: Tuple[str] = None,
        check: Optional[dict] = None,
    ):
        self._consul.agent.service.register(
            name,
            service_id=service_id,
            address=address,
            port=port,
            tags=tags,
            check=check,
        )

    def deregister(self, service_id: str):
        self._consul.agent.service.deregister(service_id)

    def get(self, key: str) -> NoneBytes:
        _, data = self._consul.kv.get(key)
        return data['Value'] if data else None

    def put(self, key: str, value: str) -> bool:
        return self._consul.kv.put(key, value)


def setup_consul(app: FastAPI, config: dict):
    consul = ConsulService(config['consul_uri'])
    setattr(app, 'consul', consul)

    # configuration settings from consul
    database_uri = consul.get('wazo-router-confd.database_uri')
    if database_uri is not None:
        config['database_uri'] = database_uri.decode('utf-8')

    # register the API HTTP service on consul
    service_id = 'wazo-router-confd-%s' % uuid4()

    # pylint: disable= unused-variable
    @app.on_event("startup")
    def startup_event():
        consul = getattr(app, 'consul')
        consul.register(
            service_id,
            'wazo-router-confd',
            address=config.get('advertise_host'),
            port=config.get('advertise_port'),
            tags=('wazo-router-confd', 'wazo-router', 'wazo-api', 'wazo'),
            check={
                "id": "api",
                "name": "HTTP API on port 5000",
                "http": "http://%(advertise_host)s:%(advertise_port)d/status" % config,
                "method": "GET",
                "interval": "10s",
                "timeout": "1s",
            }
            if (config.get('advertise_host') and config.get('advertise_port'))
            else None,
        )

    # pylint: disable= unused-variable
    @app.on_event("shutdown")
    def shutdown_event():
        consul = getattr(app, 'consul')
        consul.deregister(service_id)

    return app
