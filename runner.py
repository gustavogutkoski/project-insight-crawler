import os
import sqlite3

from crawler.database.database import create_tables
from crawler.logger.logger import setup_logger
from crawler.parser.java_parser import parse_java_file
from crawler.use_cases.save_data import save_project_data

logger = setup_logger(__name__)


def run_crawler(project_path: str, db_path: str = "crawler.db") -> None:
    logger.info(f"Starting crawler on project: {project_path}")

    conn = sqlite3.connect(db_path)
    logger.debug(f"Connected to database at: {db_path}")
    create_tables(conn)

    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                logger.info(f"Analyzing file: {file_path}")

                try:
                    results = parse_java_file(file_path)
                    logger.debug(f"Parsed {len(results)} items from {file_path}")
                    save_project_data(conn, results)
                except ValueError as e:
                    logger.error(f"Parsing error in {file_path}: {e}", exc_info=True)
                except sqlite3.DatabaseError as e:
                    logger.error(
                        f"Database error when saving data from {file_path}: {e}", exc_info=True
                    )
                except (OSError, IOError) as e:
                    logger.error(f"File error with {file_path}: {e}", exc_info=True)
                except Exception as e:
                    logger.error(f"Unexpected error processing {file_path}: {e}", exc_info=True)
                    raise

    conn.close()
    logger.info("Crawler done!")
