from providers.database.functions import run_tasks


async def run_migrations():
    """
    Runs the migration tasks
    """
    await run_tasks("migrations", "Migration", "Schema")