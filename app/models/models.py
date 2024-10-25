from sqlmodel import Field, SQLModel

class UserBase(SQLModel):
    nome: str = Field(nullable=False, index=True)
    email: str = Field(nullable=False, index=True)
    senha: str = Field(nullable=False)

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True, nullable=False)

class UserPublic(SQLModel):
    id: int
    nome: str
    email: str

class UserCreate(UserBase):
    pass

class LoginData(SQLModel):
    email: str
    senha: str