from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import culture, search
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含API路由
app.include_router(culture.router, prefix="/api/v1/culture", tags=["culture"])
app.include_router(search.router, prefix="/api/v1/search", tags=["search"])

@app.get("/")
async def root():
    return {"message": "欢迎使用民宿文化平台API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}