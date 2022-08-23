import os
import pymongo

# Get DB environment variables
MONGO_HOST = os.getenv("MONGO_HOST", "0.0.0.0")
MONGO_PORT = int(os.getenv("MONGO_PORT", "27017"))


def get_db_connection(host: str=MONGO_HOST, port: int=MONGO_PORT) -> pymongo.MongoClient:
    """
    Gets a DB connection to the MongoDB server

    Parameters
    ----------
    host : str, optional
        The address to connect to, by default MONGO_HOST
    port : int, optional
        The port to connect to, by default MONGO_PORT

    Returns
    -------
    pymongo.MongoClient
        The DB connection to the MongoDB server

    Raises
    ------
    Exception
        This exception is raised if the DB connection fails
    """
    client = pymongo.MongoClient(host, port)

    try:
        client.server_info()
    except:
        raise Exception("Failed to get DB connection!")

    return client
