from smrp.db import pool
from smrp.models import Role
from typing import List


class RoleService:
    
    async def find_all(self, sortby: str, sortdir: str) -> List[Role]:
        lx: List[Role] = []
        async with pool.acquire() as conn:
            rows = await conn.fetch(f"""
                select id, name from role order by {sortby} {sortdir}
            """)
            lx = [Role(**dict(row)) for row in rows]
        
        return lx
    
    async def find_by_id(self, id: int) -> Role | None:
        async with pool.acquire() as conn:
            row = await conn.fetchrow(f"""
                select id, name from role where id = $1 limit 1
            """, id)
            if row:
                return Role(**dict(row))

        return None
