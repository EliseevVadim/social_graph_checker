import pandas as pd


def create_dataframe(data, keys):
    filtered_data = [{k: v for k, v in item.items() if k in keys} for item in data]
    df = pd.DataFrame(filtered_data, columns=keys)
    return df


def convert_to_hours_and_minutes(decimal_hours):
    hours = int(decimal_hours)
    minutes = int((decimal_hours - hours) * 60)
    return hours, minutes

