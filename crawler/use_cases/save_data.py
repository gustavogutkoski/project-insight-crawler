import sqlite3
from typing import List, Tuple

from crawler.database.database import insert_class, insert_method
from crawler.logger.logger import setup_logger
from crawler.models.class_info import ClassInfo
from crawler.models.method_info import MethodInfo

logger = setup_logger(__name__)


def save_project_data(
    conn: sqlite3.Connection, results: List[Tuple[ClassInfo, List[MethodInfo]]]
) -> None:
    for cls, methods in results:
        try:
            class_id = insert_class(conn, cls)
            logger.info(f"Class '{cls.name}' saved with ID {class_id}")

            for mtd in methods:
                mtd.class_id = class_id
                insert_method(conn, mtd)
                logger.debug(f"Method '{mtd.method_name}' saved under class ID {class_id}")

        except Exception:
            logger.error(f"Error saving data for class '{cls.name}'", exc_info=True)
