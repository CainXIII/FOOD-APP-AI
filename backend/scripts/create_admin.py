"""
Create admin user for testing
"""
import asyncio
from app.database import get_db
from app.models.user import User, UserRole
from app.core.security import hash_password
from sqlalchemy import select

async def create_admin():
    async for db in get_db():
        # Check if admin exists
        result = await db.execute(
            select(User).where(User.email == "admin@cooking.app")
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            print("✓ Admin user already exists")
            # Update to ensure role is ADMIN
            if existing.role != UserRole.ADMIN:
                existing.role = UserRole.ADMIN
                await db.commit()
                print("✓ Updated user to admin")
        else:
            # Create new admin
            admin = User(
                email="admin@cooking.app",
                password_hash=hash_password("Admin1234"),
                full_name="Admin User",
                role=UserRole.ADMIN,
                is_active=True
            )
            db.add(admin)
            await db.commit()
            print("✓ Admin user created successfully")
            print(f"  Email: admin@cooking.app")
            print(f"  Password: Admin1234")
        
        break

if __name__ == "__main__":
    asyncio.run(create_admin())
