import os
from typing import get_type_hints, Union
from dotenv import load_dotenv

load_dotenv()

class AppConfigError(Exception):
    pass

def _parse_bool(val: Union[str, bool]) -> bool:
    return val if isinstance(val, bool) else val.lower() in [
        'true', 
        'yes', 
        '1'
    ]

class AppConfig:
    DEBUG: bool = False
    ENV: str = 'production'
    AWS_REGION: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_ACCESS_KEY_ID: str
    CSV_HEADER: str
    VALID_DOMAINS: str

    def __init__(self, env):
        for field in self.__annotations__:
            if not field.isupper():
                continue

            default_value = getattr(self, field, None)
            if default_value is None and env.get(field) is None:
                raise AppConfigError('The {field} field is required')

            try:
                var_type = get_type_hints(AppConfig)[field]
                if var_type == bool:
                    value = _parse_bool(env.get(field, default_value))
                else:
                    value = var_type(env.get(field, default_value))

                self.__setattr__(field, value)
            except ValueError as e:
                raise AppConfigError(
                    'Unable to cast value of \
                        "{env[field]}" to type \
                            "{var_type}" for "{field}" field'
                    ) from e

    def __repr__(self):
        return str(self.__dict__)

config = AppConfig(os.environ)
