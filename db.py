from typing import List, Optional
import pyotp
from totp import totp
from merkly.mtree import MerkleTree
from datetime import datetime
from model import *


user_to_secret = {}
# user to list of TimestampToOtp
user_to_timestamp_to_otp = {}
user_to_merkle_tree = {}


def print_user_to_secret():
    print(f"user_to_secret: {user_to_secret}")


def register_user(username: str, issuer_name: str = 'CoolWallet') -> str:
    # Create a new TOTP object
    totp = pyotp.TOTP(pyotp.random_base32())

    # Store the secret for this user
    user_to_secret[username] = totp.secret
    user_to_timestamp_to_otp[username] = []

    # Generate a provisioning URI that can be used to configure the Google Authenticator app
    return totp.provisioning_uri(name=username, issuer_name=issuer_name)


def verify_otp(username: str, otp: str) -> bool:
    secret = user_to_secret.get(username)

    if not secret:
        return False

    # Create a TOTP object with the user's secret
    totp = pyotp.TOTP(secret)

    # Verify the OTP
    return totp.verify(otp)


def generate_totp_for_timestamp(username, timestamp):
    secret = user_to_secret.get(username)
    totp_code = totp(key=secret, unix_timestamp=timestamp)
    user_to_timestamp_to_otp[username].append((TimestampToOtp(timestamp=timestamp, otp=totp_code)))
    print(f"user_to_timestamp_to_otp: {user_to_timestamp_to_otp}")
    user_merkle_leafs = [item.otp for item in user_to_timestamp_to_otp[username]]
    print(f"user_merkle_leafs: {user_merkle_leafs}")
    # create a Merkle Tree
    mtree = MerkleTree(user_merkle_leafs)
    user_to_merkle_tree[username] = mtree
    print(f"user_to_merkle_tree: {user_to_merkle_tree}")
    return totp_code

def get_next_leaf_and_proof_for_user(username):
    user_mtree = user_to_merkle_tree[username]
    leaf = get_leaf_for_next_timestamp(username)
    proof = user_mtree.proof(leaf)
    proof_cast_str = str(proof)
    print(f"leaf: {leaf}")
    print(f"proof: {proof}")
    print(f"proof_cast_str: {proof_cast_str}")
    return NextLeafForUserResponse(proof = proof_cast_str, leaf = leaf)

def get_leaf_for_next_timestamp(username):
    user_timestamps = [item.timestamp for item in user_to_timestamp_to_otp[username]]
    closest_future_timestamp = get_closest_future_timestamp(user_timestamps)
    return get_otp_for_timestamp(user_to_timestamp_to_otp[username], closest_future_timestamp)

def get_closest_future_timestamp(timestamps):
    now = datetime.now()
    # Filter timestamps in the future
    future_timestamps = [ts for ts in timestamps if datetime.fromtimestamp(ts) > now]
    if not future_timestamps:
        return None
    # Get the closest future timestamp
    closest_future_timestamp = min(future_timestamps, key=lambda ts: datetime.fromtimestamp(ts) - now)
    return closest_future_timestamp

def get_otp_for_timestamp(timestamp_to_otp_list: List[TimestampToOtp], input_timestamp: int) -> Optional[str]:
    for item in timestamp_to_otp_list:
        if item.timestamp == input_timestamp:
            return item.otp
    return None