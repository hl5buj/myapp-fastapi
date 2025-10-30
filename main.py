from fastapi import FastAPI, Depends
from typing import Dict
from auth import get_current_user

app = FastAPI(title="TaskHub FastAPI")

@app.get("/")
def read_root():
    """헬스 체크 엔드포인트"""
    return {"message": "TaskHub FastAPI 서버가 실행 중입니다"}

@app.get("/protected")
def protected_route(current_user: Dict = Depends(get_current_user)):
    """보호된 엔드포인트 - 로그인 필요"""
    return {
        "message": "인증 성공!",
        "user_id": current_user["user_id"]
    }

@app.post("/upload")
def upload_file(current_user: Dict = Depends(get_current_user)):
    """파일 업로드 API (인증 필요)"""
    return {
        "message": "파일 업로드 준비 완료",
        "user_id": current_user["user_id"],
    }