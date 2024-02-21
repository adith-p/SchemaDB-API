from fastapi import FastAPI,Depends,status
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from sqlalchemy import text
from databases.database import get_db


from schema.schema import TableSchema
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
    
    return {'message':'message'}

@app.get('/fetch-data/{table_name}')
def fetch_table(table_name:str, limit: int = 10, offset: int = 1,db: Session = Depends(get_db)):
    
    
    if does_table_exist(table_name): # check if the table exist
        sql = db.execute(text(f' SELECT * FROM {table_name} LIMIT :limit OFFSET :offset'),{'limit':limit,'offset':offset})
        result = sql.all()    
        serialized_data = dynamic_serialization(sql, result)
        
        return JSONResponse(serialized_data)
    
    return {'message': f' the table {table_name} does not exist','code':status.HTTP_404_NOT_FOUND}
    