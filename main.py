import cv2
from fastapi import FastAPI
from pydantic import BaseModel
from passlib.context import CryptContext
from datetime import datetime

# database with user
user_db = {
    "julia": {
        "username": "julia",
        # password: Julia123
        "hashed_password": "$2a$12$uLxNY9Vz2QGAZAKyUVl4R.zkXXXq56QtdKPC0oTVL1bt50fkDI0sW"
    }
}


# users model with two fields
class User(BaseModel):
    username: str
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return User(**user_dict)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


@app.get("/")
async def root():
    return {"Hello user, these are the functions of this app which you can try yourself: "
            " - Check if given number is prime: https://python-project.herokuapp.com/prime/{number}"
            " - Check the current time after give credentials: "
            " https://python-project.herokuapp.com/user/time?username={username}&password={password}"}
#    return {"Hello user, here you can test available functions: http://127.0.0.1:8000/docs#"}


# endpoint checks if number is prime
@app.get("/prime/{number}")
async def is_prime(number):
    try:
        number = int(number)
        for n in range(2, int(number**0.5)+1):
            if number % n == 0:
                return {"message": f"Number {number} is not prime"}
        return {"message": f"Number: {number} is prime"}
    except ValueError:
        return {"message": "Input is not an integer"}


# endpoint inverts colour of the picture which is given by the path
# @app.post("/picture/invert")
# async def invert_picture(pathname: str):
#    image = cv2.imread(pathname)
#    new_image = cv2.bitwise_not(image)
#    tmp = cv2.imwrite('files/newpicture.png', new_image)
#    return {"message": f"Saving: {tmp}"}


# endpoint which gives current date after authenticate user with username and password
@app.get("/user/time")
async def get_time(username: str, password: str):
    user = authenticate_user(user_db, username, password)
    if user:
        current_time = datetime.now()
        time = current_time.strftime("%H:%M:%S")
        return {"message": f"User {username} is here! Your time is {time} "}
    else:
        return {"message": "Wrong username or password"}
