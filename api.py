from fastapi import FastAPI
from db import register_user, verify_otp, print_user_to_secret, generate_totp_for_timestamp, get_next_leaf_and_proof_for_user, generate_totp_batch
from model import *
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/users", response_model=UserUrl)
async def post_user(user: User):
    return UserUrl(url=register_user(user.name))

@app.get("/verify_otp/{username}/{otp}", response_model=OtpVerification)
async def verify(username, otp):
    return OtpVerification(verified=verify_otp(username, otp))

@app.post("/generate_otp_for_timestamp", response_model=GenerateOtpResponse)
async def generate_otp(input: GenerateOtp):
    return GenerateOtpResponse(otp=generate_totp_for_timestamp(input.user, input.timestamp))

# TODO return root of tree
@app.post("/generate_otp_batch", response_model=MTreeRoot)
async def generate_otp_batch(input: GenerateOtp24Hours):
    root=generate_totp_batch(input.user)
    return MTreeRoot(root=root)

@app.get("/next_leaf_for_user/{username}", response_model=NextLeafForUserResponse)
async def next_leaf_for_user(username):
    res = get_next_leaf_and_proof_for_user(username)
    return NextLeafForUserResponse(leaf=res.leaf,proof=res.proof)