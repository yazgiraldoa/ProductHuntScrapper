import os
import pandas as pd
from pyairtable import Table
from productHuntManager import organize_info_to_df


def connect_to_airtable():
    """Function that connects to Airtable API"""

    api_key = "Secret"
    table_name = "Products"
    base_id = "Secret"
    table = Table(api_key, base_id, table_name)
    return table


def create(table):
    """Function that gets the data from Product Hunt
    and uploads the records in Airtable"""
    df = organize_info_to_df()
    df = df.fillna('')
    df = df.applymap(str)
    fields = df.to_dict('records')
    table.batch_create(fields, typecast=True)


if __name__ == '__main__':
    table = connect_to_airtable()
    create(table)
