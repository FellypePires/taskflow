"""TaskFlow: API REST simples de tarefas (projeto-base da disciplina DevOps Tools).

Os dados ficam em memória: ao reiniciar a API, as tarefas somem.
Isso é proposital nesta fase; o foco da disciplina é a automação em volta do código.
"""

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="TaskFlow",
    description="API de tarefas usada no projeto evolutivo de DevOps Tools (ADS/UNIPAR).",
    version="0.1.0",
)


class TaskIn(BaseModel):
    title: str = Field(min_length=1, max_length=120, examples=["Estudar Git"])
    done: bool = False


class Task(TaskIn):
    id: int


_tasks: dict[int, Task] = {}
_next_id = 1


def reset_db() -> None:
    """Limpa os dados em memória (usado pelos testes)."""
    global _next_id
    _tasks.clear()
    _next_id = 1


@app.get("/tasks", response_model=list[Task])
def list_tasks(done: bool | None = None) -> list[Task]:
    tasks = list(_tasks.values())
    if done is not None:
        tasks = [task for task in tasks if task.done == done]
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    if task_id not in _tasks:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return _tasks[task_id]


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskIn) -> Task:
    global _next_id
    task = Task(id=_next_id, **payload.model_dump())
    _tasks[task.id] = task
    _next_id += 1
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, payload: TaskIn) -> Task:
    if task_id not in _tasks:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    task = Task(id=task_id, **payload.model_dump())
    _tasks[task_id] = task
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int) -> Response:
    if _tasks.pop(task_id, None) is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
