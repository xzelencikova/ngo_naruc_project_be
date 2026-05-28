from pydantic import BaseModel, EmailStr


class UserAuthDTO(BaseModel):
    email: EmailStr
    password: str


class UserDTO(BaseModel):
    id: int
    email: EmailStr
    name: str
    surname: str
    role: str


class UserRegistrationDTO(UserDTO):
    password: str
