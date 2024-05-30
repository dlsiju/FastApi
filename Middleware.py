

from fastapi import FastAPI,Request


fastapi = FastAPI()

class Middleware:

    @fastapi.middleware('http')
    async def method_middleware(request: Request, call_next):
        print('middleware called in different class')
        response = await call_next(request)
        return response


