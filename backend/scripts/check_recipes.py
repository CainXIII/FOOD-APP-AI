import asyncio
from app.database import get_db
from app.models.recipe import Recipe
from sqlalchemy import select

async def check():
    async for db in get_db():
        result = await db.execute(select(Recipe))
        recipes = result.scalars().all()
        print(f'Total recipes: {len(recipes)}')
        for r in recipes:
            print(f'  - {r.title_vi} (published={r.is_published})')
        break

asyncio.run(check())
