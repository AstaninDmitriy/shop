from fastapi import FastAPI

from users.views import router as users_router

app = FastAPI(title='Shop')
app.include_router(users_router)


@app.get('/')
def hello_user():  # noqa
    return {
        'message': 'hello, user!',
    }
