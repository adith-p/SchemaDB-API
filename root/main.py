from fastapi import FastAPI,Depends,status
from fastapi.responses import JSONResponse


from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError,ProgrammingError
from databases.database import get_db


from schema.schema import TableSchema,Insert_data
from utils.sql_dtypes import create_sql
from utils.dynamic_serializers import does_table_exist,dynamic_serialization

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
def fetch_table(table_name:str, limit: int = 10, offset: int = 1,db: Session = Depends(get_db)):
    

    if does_table_exist(table_name): # check if the table exist
        sql = db.execute(text(f' SELECT * FROM "db.{table_name}" LIMIT :limit OFFSET :offset'),{'limit':limit,'offset':offset})
        result = sql.all()    
        serialized_data = dynamic_serialization(sql, result)
        
        return JSONResponse(serialized_data)
    
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
async def insert_data(table_name:str,insert_item:Insert_data,db: Session = Depends(get_db)):

    cols = [i for i in insert_item.items.keys()]
    values = [i for i in insert_item.items.values()]
        
    if does_table_exist(table_name):
        
        sql = f"INSERT INTO {table_name} ("
        sql += ", ".join(cols)
        sql += ") VALUES ("
        sql += ", ".join([f"'{i}'" if i not in ['default', 'current_timestamp','null'] else i for i in values])
        sql += ")"
        try:
            db.execute(text(sql))
            db.commit()
        except (ProgrammingError, IntegrityError) as e:
            db.rollback()
            return {'message': f'error while inserting data into table {table_name}', 'code': status.HTTP_400_BAD_REQUEST, 'error': str(e)}

        return {"message": "Data inserted successfully"}