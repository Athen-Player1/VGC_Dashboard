from __future__ import annotations

import logging
import time

from app.db import init_db
from app.services.meta_store import initialize_meta_store
from app.services.simulation_runner import run_simulation_job
from app.services.simulation_store import (
    claim_next_simulation_job,
    complete_simulation_job,
    fail_simulation_job,
)
from app.services.team_store import initialize_team_store


logging.basicConfig(level=logging.INFO, format="[sim-worker] %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    init_db()
    initialize_team_store()
    initialize_meta_store()
    logger.info("Worker online")

    while True:
        job = claim_next_simulation_job()
        if job is None:
            time.sleep(2)
            continue

        try:
            logger.info("Running job %s against %s", job["id"], job["opponent_label"])
            summary = run_simulation_job(job)
            complete_simulation_job(job["id"], summary, int(job["requested_games"]))
            logger.info("Completed job %s", job["id"])
        except Exception as exc:  # pragma: no cover
            logger.exception("Job %s failed", job["id"])
            fail_simulation_job(job["id"], str(exc))


if __name__ == "__main__":
    main()
