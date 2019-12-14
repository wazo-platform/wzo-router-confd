# Copyright 2019 The Wazo Authors  (see the AUTHORS file)
# SPDX-License-Identifier: GPL-3.0-or-later

from fastapi import FastAPI

from .consul import setup_consul
from .database import setup_database, setup_aiopg_database, upgrade_database
from .redis import setup_redis
from .routers import carriers
from .routers import carrier_trunks
from .routers import cdr
from .routers import dids
from .routers import domains
from .routers import kamailio
from .routers import ipbx
from .routers import normalization
from .routers import routing_rules
from .routers import routing_group
from .routers import tenants


def get_app(config: dict):
    app = FastAPI()
    if config.get('consul_uri') is not None:
        app = setup_consul(app, config)
    app = setup_database(app, config)
    app = setup_aiopg_database(app, config)
    if config.get('database_upgrade'):
        upgrade_database(app, config)
    app = setup_redis(app, config)
    app.include_router(carriers.router)
    app.include_router(carrier_trunks.router)
    app.include_router(cdr.router)
    app.include_router(dids.router)
    app.include_router(domains.router)
    app.include_router(ipbx.router)
    app.include_router(kamailio.router)
    app.include_router(normalization.router)
    app.include_router(routing_rules.router)
    app.include_router(routing_group.router)
    app.include_router(tenants.router)

    return app
