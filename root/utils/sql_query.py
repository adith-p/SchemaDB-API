from schema.schema import Search_data, TableSchema


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