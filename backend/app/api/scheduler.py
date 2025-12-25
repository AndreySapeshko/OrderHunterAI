import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timezone, timedelta
from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_EXECUTED

from backend.app.ingestion.tasks import run_all_sources

logger = logging.getLogger(__name__)


scheduler = AsyncIOScheduler()
def job_listener(event):
    if event.exception:
        logger.exception(
            "Job %s failed", event.job_id, exc_info=event.exception
        )
    else:
        logger.info("Job %s executed successfully", event.job_id)

scheduler.add_listener(
    job_listener,
    EVENT_JOB_ERROR | EVENT_JOB_EXECUTED,
)


def setup_scheduler():
    # scheduler.add_job(
    #     run_all_sources,
    #     IntervalTrigger(minutes=15),
    #     id="run_sources_ingestion",
    #     replace_existing=True,
    #     max_instances=1,
    #     coalesce=True,
    # )

    scheduler.add_job(
        lambda: logger.info("SCHEDULER TEST JOB EXECUTED"),
        trigger="date",
        run_date=datetime.now(tz=timezone.utc) + timedelta(seconds=5),
    )

    scheduler.add_listener(
        job_listener,
        EVENT_JOB_ERROR | EVENT_JOB_EXECUTED,
    )
