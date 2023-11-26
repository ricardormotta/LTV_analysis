from start_kedro_session import get_kedro_catalog

catalog = get_kedro_catalog()

base = catalog.load("base")
xs = catalog.load("xs")
