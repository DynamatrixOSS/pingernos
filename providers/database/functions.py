import importlib
import os

from config.directories import Directories
from database.executioners.database import execute
from providers.modifiers.logger import setup_logger

logger = setup_logger()


async def run_tasks(directory_name, task_name, task_type):
    """
    Collects all the task files from the specified directory and dynamically loads the classes,
    retrieving the desired data for the task.
    """

    task_directory = Directories().get_directory(directory_name)
    task_files = os.listdir(task_directory)

    for file in task_files:
        if not file.endswith(".py"):
            continue

        task_name = file.split(".")[0]
        task_path = os.path.join(task_directory, file)

        spec = importlib.util.spec_from_file_location(task_name, task_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, task_type):
            raise AttributeError(f"{task_type} class not found in {task_name}")

        task_class = getattr(module, task_type)

        task_instance = task_class()

        task_data = {
            "name": task_instance.get_table() if task_type == "Seeder" else task_instance.get_name(),
            "data": task_instance.get_columns()
        }

        logger.info(f'Running {task_name} {task_type}...')

        if task_type == "Seeder":
            await task_handler(task_data, task_type)
        elif task_type == "Schema":
            await task_handler(task_data, task_type)

        logger.info(f'Finished running {task_name} {task_type}.')


async def task_handler(task_data, task_type):
    """
    Runs the appropriate task based on the task type (Seeder or Schema)
    """
    if task_type == "Seeder":
        query_string = seed_query_builder(task_data["name"], task_data["data"])
        await execute(query_string[0], query_string[1])
    elif task_type == "Schema":
        query_string = migration_query_builder(task_data["name"], task_data["data"])
        await execute(query_string)


def seed_query_builder(table_name, columns_list):
    """
    Builds a query string for inserting data into a table
    """
    keys_list = [key for row in columns_list for key in row.keys()]
    keys_string = ", ".join(keys_list)
    values_list = [str(value) for row in columns_list for value in row.values()]

    placeholders = ", ".join(["%s"] * len(values_list))
    query_string = f"INSERT IGNORE INTO {table_name} ({keys_string}) VALUES ({placeholders})"

    return query_string, tuple(values_list)


def migration_query_builder(table_name, columns):
    """
    Builds a query string for creating a table
    """
    query = f"CREATE TABLE IF NOT EXISTS {table_name} ("
    for column in columns:
        query += f"{column}, "
    query = query[:-2]
    query += ")"
    return query


async def run_seeders():
    """
    Runs the seeder tasks
    """
    await run_tasks("seeders", "Seeder", "Seeder")


async def run_migrations():
    """
    Runs the migration tasks
    """
    await run_tasks("migrations", "Migration", "Schema")
