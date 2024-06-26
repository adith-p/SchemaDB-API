from pydantic import BaseModel
# from enum import Enum
from typing import Literal,Optional


"""
column:[
    {
    name:str,
    dtype:(int,float,str,datetime,bool,None),
    default:None,
    primary_key:bool,
    autoincrement:bool,
    nullable:bool,
    },
]
"""


class ColumnSchema(BaseModel):
    name:str
    dtype: Literal['int','str','bool','float','date','time','timestamp']
    primary_key:Optional[bool]=False
    nullable:Optional[bool]=True
    default:Optional[str] = ""
    


class TableSchema(BaseModel):
    tbl_name:str
    column:list[ColumnSchema]
    
    
class Insert_data(BaseModel):   
    items:dict  

class Bulk_insert(BaseModel):
    items:list[dict]
    
    
class Schema_data(BaseModel):
    tbl_name:str
    column:list[dict]
    
    
class Search_data(BaseModel):
    col_name:str
    ilike:bool = True
    search_value:str
    
class Join_data(BaseModel):
    table_name:str
    join_table_name:str
    join_type:Literal['left','right','inner','full'] = 'inner'
    table_name_col:str
    join_table_name_col:str