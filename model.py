from typing import List
from pydantic import BaseModel
from merkly.mtree import Node

class User(BaseModel):
    name: str

class UserUrl(BaseModel):
    url: str

class OtpVerification(BaseModel):
    verified: bool

class GenerateOtp(BaseModel):
    user: str
    timestamp: int

class GenerateOtpResponse(BaseModel):
    otp: str

class NextLeafForUserResponse(BaseModel):
    leaf: str
    # proof: List[Node]
    proof: str

class TimestampToOtp(BaseModel):
    timestamp: int
    otp: str