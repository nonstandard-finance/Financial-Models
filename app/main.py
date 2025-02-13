from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi.openapi.utils import get_openapi
from scalar_fastapi import get_scalar_api_reference


# from app.monitoring.services import request_attributes_mapper, monitoring
# from app.auth.routes import router as auth_router
from app.bankruptcy_pred.routes import router as bankruptcy_pred_router
from app.cashflow.routes import router as cashflow_router


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Financial Models | Main",
        version="1.0.0",
        description="We help you understand your data",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }
    openapi_schema["security"] = [{"Bearer": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = FastAPI()

# monitoring.instrument_fastapi(app, request_attributes_mapper=request_attributes_mapper)
# monitoring.instrument_system_metrics()

app.openapi = custom_openapi
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/verify-code/")


@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    """
    Redirects users from the root endpoint to the docs endpoint.
    """
    return RedirectResponse(url="/docs")


@app.get("/health")
def read_root():
    return {"Hello": "Service is live"}


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )


app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(auth_router, prefix="/auth", tags=["AUTH"])
app.include_router(bankruptcy_pred_router, prefix="/bankruptcy", tags=["Bankruptcy"])
app.include_router(cashflow_router, prefix="/cashflow", tags=["Cash Flow"])

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
