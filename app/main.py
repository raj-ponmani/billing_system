import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import billing, purchases
from app.database import engine, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database tables created (if not exist).")

    yield  # Application runs here

    # Shutdown logic
    await engine.dispose()
    print("🛑 Database engine disposed.")


app = FastAPI(title="Billing System", lifespan=lifespan)

# Mount static
# static_dir = os.path.join(os.path.dirname(__file__), "static")
# if os.path.isdir(static_dir):
#     app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include routes
app.include_router(billing.router, prefix="")
app.include_router(purchases.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
