from starlette.responses import JSONResponse


async def exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})
