from enum import Enum


class PassKeyLifetimeEnum(str, Enum):
    """
    Represents the time duration for the **pass_key_lifetime** field of the **SecretBase** model.
    """
    one_week = "P7D"
    three_days = "P3D"
    one_day = "P1D"
    twelve_hours = "PT12H"
    six_hours = "PT6H"
    three_hours = "PT3H"
    one_hour = "PT1H"
    thirty_minutes = "PT30M"
    five_minutes = "PT5M"
    one_minute = "PT1M"
