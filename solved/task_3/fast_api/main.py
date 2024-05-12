from datetime import date

from fastapi import FastAPI
from models import Project, Task
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///./app.db')
Session = sessionmaker(bind=engine)
session = Session()


app = FastAPI()


@app.get("/projects/")
def get_projects():
    project = session.query(Project).all()
    return project


@app.get("/project/{project_id}/")
def get_project(project_id: int):
    project = session.query(Project).filter_by(id=project_id).first()
    tasks = session.query(Task).filter_by(project_id=project_id).all()
    project.tasks = tasks
    return project


@app.post("/projects/")
def post_projects(name: str, description: str):
    project = Project(name=name, description=description)
    session.add(project)
    session.commit()
    return {"status": "success"}


@app.put("/projects/")
def post_project(project_id: int, name: str, description: str):
    project = session.query(Project).filter_by(id=project_id).first()
    project.name = name
    project.description = description
    session.commit()
    return {"status": "success"}


@app.delete("/projects/")
def delete_project(project_id: int):
    project = session.query(Project).filter_by(id=project_id).first()
    session.delete(project)
    return {"status": "success"}


@app.get("/tasks/")
def get_tasks():
    task = session.query(Task).all()
    return task


@app.get("/task/{task_id}/")
def get_task(task_id: int):
    task = session.query(Task).filter_by(id=task_id).first()
    return task


@app.post("/tasks/")
def post_tasks(name: str, description: str, status: str, deadline: date, project_id: int):
    task = Task(name=name, description=description, status=status, deadline=deadline, project_id=project_id)
    session.add(task)
    session.commit()
    return {"status": "success"}


@app.put("/tasks/")
def post_task(task_id: int, name: str, description: str, status: str, deadline: date, project_id: int):
    task = session.query(Task).filter_by(id=task_id).first()
    task.name = name
    task.description = description
    task.status = status
    task.deadline = deadline
    task.project_id = project_id
    session.commit()
    return {"status": "success"}


@app.delete("/tasks/")
def delete_task(task_id: int):
    task = session.query(Task).filter_by(id=task_id).first()
    session.delete(task)
    return {"status": "success"}
