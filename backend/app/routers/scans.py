from datetime import datetime, timezone
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from .. import database
from ..deps import current_user
from ..schemas import AnalyzeRequest, ScanResponse
from ..services.detector import analyze_message

router=APIRouter(prefix="/api",tags=["scans"])
def present(scan):
    return {**{k:scan[k] for k in ("message","source_type","trust_score","risk_level","detected_techniques","explanation","recommendation","nlp_mode","created_at")},"id":str(scan["_id"])}
@router.post("/analyze",response_model=ScanResponse)
async def analyze(body: AnalyzeRequest,user=Depends(current_user)):
    result=analyze_message(body.message); scan={**result,"user_id":user["_id"],"message":body.message.strip(),"source_type":body.source_type,"created_at":datetime.now(timezone.utc)}
    saved=await database.database.scans.insert_one(scan); scan["_id"]=saved.inserted_id; return present(scan)
@router.get("/history",response_model=list[ScanResponse])
async def history(user=Depends(current_user)):
    return [present(s) async for s in database.database.scans.find({"user_id":user["_id"]}).sort("created_at",-1)]
@router.get("/history/{scan_id}",response_model=ScanResponse)
async def detail(scan_id:str,user=Depends(current_user)):
    if not ObjectId.is_valid(scan_id): raise HTTPException(404,"Scan not found")
    scan=await database.database.scans.find_one({"_id":ObjectId(scan_id),"user_id":user["_id"]})
    if not scan: raise HTTPException(404,"Scan not found")
    return present(scan)
@router.delete("/history/{scan_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete(scan_id:str,user=Depends(current_user)):
    if not ObjectId.is_valid(scan_id): raise HTTPException(404,"Scan not found")
    result=await database.database.scans.delete_one({"_id":ObjectId(scan_id),"user_id":user["_id"]})
    if not result.deleted_count: raise HTTPException(404,"Scan not found")
