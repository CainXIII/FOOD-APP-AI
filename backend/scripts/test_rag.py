"""
Test RAG context retrieval
"""
import asyncio
import os
import sys
sys.path.insert(0, os.getcwd())

from app.database import async_session_maker
from app.services.rag import get_rag_context

async def test_rag():
    async with async_session_maker() as session:
        result = await get_rag_context('phở bò', session, top_k=3)
        print('RAG Context Result:')
        print(f'Query: {result["query"]}')
        print(f'Total contexts: {result["total"]}')
        print(f'Search type: {result["search_type"]}')
        print('Contexts:')
        for i, ctx in enumerate(result['contexts'], 1):
            similarity = ctx.get('similarity', 'N/A')
            print(f'{i}. {ctx["title"]} (similarity: {similarity})')

if __name__ == "__main__":
    asyncio.run(test_rag())