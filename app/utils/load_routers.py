import os
import logging
import importlib.util
from fastapi import FastAPI
from typing import Optional


logging.basicConfig(level=logging.INFO,
                    format='%(levelname)s %(message)s',
                    handlers=[logging.StreamHandler()])


def load_routers(app: FastAPI, router_dir: str,
                 file_extension: Optional[str] = '.py'):
    '''
    Recursively load all routers in the specified directory.

    Args:
    app (FastAPI): The FastAPI application instance.
    router_dir (str): The directory to search for router files.
    file_extension (str, optional): The file extension to consider for router files. Defaults to '.py'.

    Example usage:
    load_routers(app, 'path/to/router_directory')
    '''
    for root, _, files in os.walk(router_dir):
        for filename in files:
            if filename.endswith(file_extension) and filename != '__init__.py':
                file_path = os.path.join(root, filename)

                try:
                    spec = importlib.util.spec_from_file_location(
                        filename[:-3], file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    if hasattr(module, 'router'):
                        app.include_router(module.router)
                        logging.info(f"Router loaded from {file_path}")
                    else:
                        logging.warning(f"No router found in {file_path}")
                except Exception as e:
                    logging.error(
                        f"Error loading router from {file_path}: {e}")
