import sys, os, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent.parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.shared.gas_client import gas_post

app = FastAPI(title="Auth Service")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class OtpSend(BaseModel):
    email: str
    suk_key: str = "bannerghatta"   # default — OTP doesn't need a specific SUK

class OtpVerify(BaseModel):
    email: str
    otp: str
    suk_key: str = "bannerghatta"

@app.get("/health")
async def health():
    return {"status": "ok", "service": "auth"}

@app.post("/auth/otp/send")
async def send_otp(payload: OtpSend):
    try:
        result = await gas_post(
            {"action": "sendAdminOtp", "email": payload.email},
            payload.suk_key
        )
        return result
    except Exception as e:
        return {"success": False, "message": str(e)}

@app.post("/auth/otp/verify")
async def verify_otp(payload: OtpVerify):
    try:
        result = await gas_post(
            {"action": "verifyAdminOtp", "email": payload.email, "otp": payload.otp},
            payload.suk_key
        )
        return result
    except Exception as e:
        return {"success": False, "message": str(e)}