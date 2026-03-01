# app/container.py
from app.controllers.student_controller import StudentController
from app.services.student_service import StudentService



class Container:
    def __init__(self):
        self._student_service = None
        self._student_controller = None

    @property
    def student_service(self):
        if self._student_service is None:
            # مش هننشئ Service هنا لأن الـ db جاي من الـ request
            # هنستخدم factory في الـ dependency
            raise NotImplementedError("Service يتم إنشاؤه per-request")
        return self._student_service

    @property
    def student_controller(self):
        if self._student_controller is None:
            raise NotImplementedError("Controller يتم إنشاؤه per-request")
        return self._student_controller