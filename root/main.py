from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from databases.database import get_db


from schema.schema import TableSchema
from utils.sql_dtypes import create_sql

app = FastAPI()

# @app.get('/')
# def get_db(db: Session = Depends(get_db)):
#     sql = text(' SELECT * FROM demo')
#     result = db.execute(sql)
#     print(result.all())
    
#     return {'message':'message'}

@app.post('/create-table')
def create_table(request:TableSchema,db: Session = Depends(get_db)):
    # create sql command using request
    sql = 'CREATE TABLE '
    sql += create_sql(request)
    print(sql)
    db.execute(text(sql))
    db.commit()
    
    return {'message':'message'}