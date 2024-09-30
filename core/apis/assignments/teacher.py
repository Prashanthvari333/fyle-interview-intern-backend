from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.libs.assertions import *
from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)

@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    if p.teacher_id in [1,2]:
        teachers_assignments = Assignment.get_assignments_by_teacher(p.teacher_id)
        teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
        return APIResponse.respond(data=teachers_assignments_dump)
    else:
        return APIResponse.respond(status_code=400, data={'message':'Teacher with Id not found'})
@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    
    if incoming_payload['grade'] not in ['A','B','C','D']:
        return APIResponse.respond(data={'error': 'ValidationError'}, status_code=400)
    
    assignment = Assignment.get_by_id(grade_assignment_payload.id)
    try:
       assert_found(assignment) 
       assert_valid(assignment)
    except:
        FyleError(status_code=404,message='FyleError')
        return APIResponse.respond(data={'error': 'FyleError'}, status_code=404)
    if assignment.state in ['DRAFT'] or assignment.teacher_id != p.teacher_id:
        return APIResponse.respond(data={'error': 'FyleError'}, status_code=400)
    else:
        graded_assignment = Assignment.mark_grade(
            _id=grade_assignment_payload.id,
            grade=grade_assignment_payload.grade,
            auth_principal=p
        )
        db.session.commit()
        graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
        return APIResponse.respond(data=graded_assignment_dump)
