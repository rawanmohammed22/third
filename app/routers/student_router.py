from fastapi import APIRouter, HTTPException, Depends
from app.schemas.student_schema import StudentBase
from app.controllers.student_controller import StudentController
from app.dependencies import get_student_controller

router = APIRouter()


@router.get("/")
def get_students(
    controller: StudentController = Depends(get_student_controller)
):
    return controller.get_all_students()


@router.post("/")
def add_student(
    student: StudentBase,
    controller: StudentController = Depends(get_student_controller)
):
    try:
        student_id = controller.add_student(
            student.name, student.age, student.email
        )
        return {"id": student_id, "message": "Student added successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/{student_id}")
def update_student(
    student_id: int,
    student: StudentBase,
    controller: StudentController = Depends(get_student_controller)
):
    try:
        controller.update_student(
            student_id, student.name, student.age, student.email
        )
        return {"message": "Student updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    controller: StudentController = Depends(get_student_controller)
):
    try:
        controller.delete_student(student_id)
        return {"message": "Student deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

