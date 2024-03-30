from schema.schema import Search_data, TableSchema,Bulk_insert,Join_data
from .db_utils import table_schema
from fastapi.responses import JSONResponse

def sql_ist(col):
    if col.dtype == 'int':
        sql = f' {col.name}'
        
        if col.primary_key:
            sql += f' SERIAL PRIMARY KEY'
        else:
            sql += ' INTEGER'
            
        if not col.nullable:
            sql += ' NOT NULL'
        
        if col.default:
            sql += f' DEFAULT {col.default}'
            
        return sql +','
    
    if col.dtype == 'timestamp':
        sql = f' {col.name}  TIMESTAMP'
        
        if col.primary_key:
            sql += ' PRIMARY KEY'
        
        if not col.nullable:
            sql += ' NOT NULL'
        
        return sql + ' DEFAULT CURRENT_TIMESTAMP,'

    if col.dtype == 'str':
        sql = f' {col.name} VARCHAR(255)' 
        
        if col.primary_key:
            sql += ' PRIMARY KEY'
            
        if not col.nullable:
            sql += ' NOT NULL'
        
        if col.default:
            sql += f' DEFAULT {col.default})'
        
        return sql + ','
        

def create_sql(request:TableSchema):
    sql = f'{(request.tbl_name)} ('
    
    for col in request.column:
        if col.dtype in ['int','str','timestamp']:
            sql += sql_ist(col)
            
            continue
            
            
        sql += f' {col.name} {col.dtype.upper()}'
        
        if col.primary_key:
            sql += ' PRIMARY KEY '
        if col.default:
            sql += f' DEFAULT {col.default} '
        if not col.nullable and col.dtype != 'bool':
            sql += ' NOT NULL '
        sql += ','
    return sql[:-1] +')'

def search_sql(table_name:str,search_data:Search_data):
    # select * from table_name where col_name (ilike) or (like) '%search_value%'
    sql = f" SELECT * FROM \"{table_name}\" WHERE \"{search_data.col_name}\" {'ilike' if search_data.ilike else 'like'} '%{search_data.search_value}%'"
    return sql

def complete_key_set(bulk_insert:Bulk_insert, col:list):
    
    for item in bulk_insert.items:
        for key in item.keys():
            if key not in col:
                col.append(key)

        for key in col:
            if key not in item:
                item[key] = 'null'

def bulk_create(table_name: str, bulk_insert: Bulk_insert):
    
    col = []
    
    complete_key_set(bulk_insert, col)

    sql = f"INSERT INTO {table_name} ("
    sql += ", ".join(col)
    sql += ") VALUES "

    values = []
    for item in bulk_insert.items:
        for key in col:
            values.append(item.get(key, 'null'))

        sql += "("
        sql += ", ".join([f"'{value}'" if value not in ['default', 'current_timestamp', 'null'] else value for value in values])
        sql += "),"
        values = []
    return sql[:-1] + f' RETURNING {table_schema(table_name).get('Schema')[0]['name']}'

def join_table(join_data:Join_data):
  
    
    
    table_name = join_data.table_name
    join_table_name = join_data.join_table_name
    join_type = join_data.join_type
    table_pk = join_data.table_name_col
    join_table_pk = join_data.join_table_name_col   
    
    if join_type == 'full':
        join_type = 'FULL OUTER'
    
    sql = f"""
        SELECT * 
        FROM {table_name}
        {join_type.upper()} JOIN {join_table_name} 
        ON {table_name}.{table_pk} = {join_table_name}.{join_table_pk}
    """
    
    return sql