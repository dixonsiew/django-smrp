from ninja import Router
from smrp.db import pool
from smrp.models import CommonSetup

router = Router(tags=["Setup/City"])

@router.get("/city/list")
async def list_city(request):
    table = 'city'
    async with pool.acquire() as conn:
        rows = await conn.fetch(f"""
            select t.id, t.code, t.desc, t.ref, t.created_by, t.created_date, t.modified_by, t.modified_date, t.deleted, t.deleted_by, t.deleted_date 
            from {table} t where t.desc <> '' and t.deleted is not true order by t.code
        """)
    return [CommonSetup(**dict(row)) for row in rows]