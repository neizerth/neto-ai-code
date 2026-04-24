"""
Роутер задач: POST /tasks, GET /tasks/{task_id} — по разбору кейса в презентации.

Слайд «APIRouter»:
  router = APIRouter(prefix="...", tags=[...])
"""

from __future__ import annotations

from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from schemas import TaskCreate, TaskResponse, _now_utc

# «хранить данные во временном списке в памяти» — из промпта POST
_tasks: list[TaskResponse] = []
_next_id: int = 1

router = APIRouter(tags=["tasks"])


@router.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_task(body: TaskCreate) -> TaskResponse:
    """
    Слайд: @router.post(...); сценарий — создание новой задачи, 201 + TaskResponse.
    """
    global _next_id
    task = TaskResponse(
        id=_next_id,
        title=body.title,
        description=body.description,
        priority=body.priority,
        created_at=_now_utc(),
    )
    _next_id += 1
    _tasks.append(task)
    return task


@router.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    responses={404: {"description": "Нет задачи", "content": {"application/json": {"example": {"detail": "Task not found", "task_id": 0}}}}},
)
async def get_task(task_id: int) -> TaskResponse | JSONResponse:
    """
    Слайд: GET /tasks/{task_id}; 200 или 404.
    Промпт «обработка ошибок»: 404 + JSON { "detail", "task_id" }.
    (Через JSONResponse тело совпадает с формулировкой; классический HTTPException
    даёт ответ вида { \"detail\": \"...\" } без отдельного task_id в корне.)
    """
    for t in _tasks:
        if t.id == task_id:
            return t
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Task not found", "task_id": task_id},
    )
