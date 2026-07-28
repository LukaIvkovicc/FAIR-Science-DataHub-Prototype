from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import routes_datasets, routes_export, routes_sequences, routes_strains, routes_taxa
from app.database import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="FAIR Scientific Data Hub Prototype",
    version="0.1.0",
    description="Compact portfolio prototype for structured scientific data and FAIR-style metadata.",
    lifespan=lifespan,
)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(routes_taxa.router)
app.include_router(routes_strains.router)
app.include_router(routes_sequences.router)
app.include_router(routes_datasets.router)
app.include_router(routes_export.router)

