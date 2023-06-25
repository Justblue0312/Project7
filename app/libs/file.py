import logging
import os

logger = logging.getLogger()


def delete_file(file_name, folder_path):
    file_path = os.path.join(folder_path, file_name)
    try:
        os.remove(file_path)
        logger.info(f"{file_name} has been deleted.")
    except FileNotFoundError:
        logger.info(f"{file_name} not found in {folder_path}.")
    except Exception as e:
        logger.error(f"{file_name} cannot be deleted. Error: {e}")
