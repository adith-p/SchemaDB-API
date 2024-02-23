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