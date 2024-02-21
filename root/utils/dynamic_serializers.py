from sqlalchemy import inspect

from databases.database import engine


def does_table_exist(table_name):
    
    if inspect(engine).has_table(table_name): # does the table exist
        return True
    return False

def dynamic_serialization(sql, result): 
    serialized_data = []
    for rows in result:
        data = dict(zip(sql.keys(),rows))
        serialized_row = data 
        serialized_data.append(serialized_row)
    return serialized_data
