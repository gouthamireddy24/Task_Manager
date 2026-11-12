from sqlalchemy.orm import Session
from models import Task
from schemas import TaskCreate, TaskUpdate


# Add a new task
def create_task(db: Session, task: TaskCreate):
    new_task = Task(
        title=task.title,
        description=task.description
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# Get all tasks
def get_all_tasks(db: Session):
    return db.query(Task).order_by(Task.id.desc()).all()


# Get one task
def get_task(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


# Update task
def update_task(db: Session, task_id: int, task: TaskUpdate):
    existing_task = get_task(db, task_id)

    if existing_task is None:
        return None

    existing_task.title = task.title
    existing_task.description = task.description

    db.commit()
    db.refresh(existing_task)

    return existing_task


# Delete task
def delete_task(db: Session, task_id: int):
    existing_task = get_task(db, task_id)

    if existing_task is None:
        return None

    db.delete(existing_task)
    db.commit()

    return existing_task


# Mark task as completed
def complete_task(db: Session, task_id: int):
    existing_task = get_task(db, task_id)

    if existing_task is None:
        return None

    existing_task.status = "Completed"

    db.commit()
    db.refresh(existing_task)

    return existing_task