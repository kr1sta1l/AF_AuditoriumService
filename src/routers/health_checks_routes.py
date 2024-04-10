from src.config import config
from fastapi_healthchecks.checks.http import HttpCheck
from fastapi_healthchecks.checks.postgres import PostgreSqlCheck
from fastapi_healthchecks.api.router import HealthcheckRouter, Probe

readiness_router = HealthcheckRouter(
    Probe(
        name="readiness",
        checks=[
            PostgreSqlCheck(host=config.AUD_DB_HOST, port=config.AUD_DB_PORT,
                            username=config.AUD_DB_USERNAME, password=config.AUD_DB_PASSWORD),
        ],
    )
)

liveness_router = HealthcheckRouter(
    Probe(
        name="liveness",
        checks=[
            HttpCheck(url=f"http://{config.AS_HOST}:{config.AS_PORT}/health")
        ],
    )
)
