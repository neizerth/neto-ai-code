from __future__ import annotations

from fastapi import FastAPI

from api.schemas import ShoppingRequest, ShoppingResponse
from services.shopping_service import build_shopping_list


app = FastAPI(title="09 scenario demo")


@app.post("/api/shopping", response_model=ShoppingResponse)
def shopping(req: ShoppingRequest) -> ShoppingResponse:
    result = build_shopping_list(req.dish, req.people, req.output_format)
    return ShoppingResponse(ok=result.ok, message=result.message)

