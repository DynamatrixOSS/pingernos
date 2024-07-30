from providers.database.functions import run_tasks


async def run_seeders():
    """
    Runs the seeder tasks
    """
    await run_tasks("seeders", "Seeder", "Seeder")
