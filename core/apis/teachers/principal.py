# core/apis/teachers/principal.py

from flask import Blueprint
from core.apis.responses import APIResponse
from core.models.teachers import Teacher
from core.apis import decorators

from .schema import TeacherSchema

principal_teachers_bp = Blueprint('principal_teachers', __name__)

@principal_teachers_bp.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of all teachers"""
    all_teachers = Teacher.query.all()
    teachers_dump = TeacherSchema().dump(all_teachers, many=True)
    return APIResponse.respond(data=teachers_dump)