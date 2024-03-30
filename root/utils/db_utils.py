from sqlalchemy import inspect

from databases.database import engine


def does_table_exist(table_name):

    return inspect(engine).has_table(table_name)


def table_schema(table_name):
    inspector = inspect(engine)
    columns = inspector.get_columns(table_name)
    return columns



def dynamic_serialization(sql, result): 
    serialized_data = []
    for rows in result:
        data = dict(zip(sql.keys(),rows))
        serialized_row = data 
        serialized_data.append(serialized_row)
    return serialized_data

def schema_serialization(schema):
    schema = {'Schema':schema}
    serialized_data = []
    s_svalues = []
    for i in schema['Schema']:
        for j in i.values():
            s_svalues.append(str(j))
        
        data = dict(zip(i.keys(),s_svalues))
        serialized_row = data
        serialized_data.append(serialized_row)
        s_svalues = []
    return serialized_data