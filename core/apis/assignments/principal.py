from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from .schema import AssignmentSchema, AssignmentGradeSchema

principal_assignments_resources = Blueprint('principal_resources', __name__)

@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of all submitted and graded assignments"""
    all_assignments = Assignment.get_all_assignments()
    assignments_dump = AssignmentSchema().dump(all_assignments, many=True)
    return APIResponse.respond(data=assignments_dump)

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade or re-grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    assignment = Assignment.get_by_id(grade_assignment_payload.id)
    if assignment.state in ["DRAFT"]:
        return APIResponse.respond(status_code=400, data={'error': 'Assignment is in draft state'})
    else:
        graded_assignment = Assignment.mark_grade(
            _id=grade_assignment_payload['id'],
            grade=grade_assignment_payload['grade'],
            auth_principal=p
        )
        db.session.commit()
        graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
        return APIResponse.respond(data=graded_assignment_dump)
