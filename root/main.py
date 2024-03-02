from fastapi import FastAPI,Depends,status
from fastapi.responses import JSONResponse


from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError,ProgrammingError
from databases.database import get_db


from schema.schema import TableSchema,Insert_data,Schema_data,Search_data,Bulk_insert
from utils.sql_query import create_sql,search_sql,bulk_create
from utils.db_utils import does_table_exist,dynamic_serialization,table_schema,schema_serialization

app = FastAPI()


@app.post('/create-table')
def create_table(request:TableSchema,db: Session = Depends(get_db)):
    # create sql command using request
    sql = 'CREATE TABLE '
    sql += create_sql(request)
    print(sql)
    db.execute(text(sql))
    db.commit()
    
    return {'message': f'table {request.tbl_name} created successfuly'}

@app.get('/fetch-data/{table_name}')
def fetch_table(table_name:str, limit: int = 10, offset: int = 0,db: Session = Depends(get_db)):
    

    if does_table_exist(table_name): # check if the table exist
        
        sql = db.execute(text(f' SELECT * FROM "{table_name}" LIMIT :limit OFFSET :offset'),{'limit':limit,'offset':offset})
        result = sql.all()    
        serialized_data = dynamic_serialization(sql, result)

        return JSONResponse(serialized_data)
    
    return {'message': f' the table {table_name} does not exist','code':status.HTTP_404_NOT_FOUND}

@app.get('/{table_name}/schema')
def get_schema(table_name:str):
    table_s = table_schema(table_name)
    try:
        schema_data = schema_serialization(table_s)
        serialized_data=Schema_data(tbl_name=table_name,column=schema_data)
        return serialized_data
    except Exception as e:
        return {'message': f'error while fetching schema for table {table_name}','code':status.HTTP_400_BAD_REQUEST,'error':str(e)}

@app.post('/{table_name}/filter')
def filter_table(table_name:str,request:Search_data,db: Session = Depends(get_db)):
    
    if does_table_exist(table_name):

        try:
            query = search_sql(table_name,request) 
            sql=db.execute(text(query))
            result = sql.all()
            print(query)
            
            serialized_data = dynamic_serialization(sql, result)
            return serialized_data
        except Exception as e:
            return {'message': f'error while fetching data from table {table_name}','code':status.HTTP_400_BAD_REQUEST,'error':str(e)}
    return {'message': f' the table {table_name} does not exist','code':status.HTTP_404_NOT_FOUND}
    



@app.delete('/{table_name}/truncate')
def truncate_table(table_name:str,db: Session = Depends(get_db)):
    
    if does_table_exist(table_name):
        try:
            sql = text(f' TRUNCATE TABLE {table_name} ')
            db.execute(sql)
            db.commit()
            return {'message': f'table {table_name} truncated successfuly','code':status.HTTP_200_OK}
        
        except (ProgrammingError, IntegrityError) as e:
            db.rollback()
            return {'message': f'error while truncating table {table_name}','code':status.HTTP_400_BAD_REQUEST,'error':str(e)}
            
    return {'message': f' the table {table_name} does not exist','code':status.HTTP_404_NOT_FOUND}
    
@app.delete('/{table_name}/delete')
def delete_table(table_name:str,db:Session = Depends(get_db)):
    
    if does_table_exist(table_name):
        try:
            sql = text(f' DROP TABLE {table_name}')
            db.execute(sql)
            db.commit()
            return {'message': f'table {table_name} deleted successfuly','code':status.HTTP_200_OK}
        except (ProgrammingError, IntegrityError) as e:
            db.rollback()
            
            return {'message': f'error while deleting table {table_name}','code':status.HTTP_400_BAD_REQUEST,'error':str(e)}
    return {'message': f' the table {table_name} does not exist','code':status.HTTP_404_NOT_FOUND}
        
# ability to added data into the table
@app.put('/{table_name}')
async def insert_data(table_name:str,insert_item:Bulk_insert, db: Session = Depends(get_db)):
    
    if does_table_exist(table_name):
        sql = bulk_create(table_name,insert_item)
        # print(sql)
        try:
            query = db.execute(text(sql))
            db.commit()
            return dynamic_serialization(query,query.all())
        except (ProgrammingError, IntegrityError) as e:
            db.rollback()
            return {'message': f'error while inserting data into table {table_name}', 'code': status.HTTP_400_BAD_REQUEST, 'error': str(e)}
        
        
        