import os
from dotenv import load_dotenv


def env_var_loader(file_name, file_path=None):
    """
    Load environment variables from a specified file using python-dotenv.

    Args:
        file_name (str): The name of the environment file.
        file_path (str, optional): The path to the directory containing the environment file.
    """
    if file_path:
        env_path = os.path.join(file_path, file_name)
    else:
        wd = os.getcwd()
        env_path = os.path.join(wd, file_name)

    if os.path.isfile(env_path):
        load_dotenv(dotenv_path=env_path)


env_var_loader("tests/.env")
