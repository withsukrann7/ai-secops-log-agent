from pydantic import BaseModel, Field

class LogInputSchema(BaseModel):
    pid: int = Field(..., description="Log kaydına ait İşlem ID (Process ID)")
    port: int = Field(..., description="Bağlantı kurulan hedef port numarası")

    class Config:
        json_schema_extra = {
            "example": {
                "pid": 72734,
                "port": 52971
            }
        }