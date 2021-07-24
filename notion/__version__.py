def get_version():
    try:
        version = __import__("pkg_resources").get_distribution("notion-sdk").version
    except Exception:
        version = "unknown"
    return version


__author__ = "Nicolas Lecoy"
__author_email__ = "nicolas@syncr.so"
__copyright__ = "Copyright 2021 Syncr Inc"
__description__ = "A simple and easy to use Python client for the Notion API."
__license__ = "Apache 2.0"
__title__ = "notion-sdk"
__version__ = get_version()
__url__ = "https://github.com/getsyncr/notion-sdk"
