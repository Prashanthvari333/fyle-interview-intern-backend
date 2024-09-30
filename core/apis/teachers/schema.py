# core/apis/teachers/schema.py

from marshmallow import Schema, fields,post_load
from core.models.teachers import Teacher
from core.models.users import User
from core.libs.helpers import GeneralObject

class TeacherSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(required=True)
    user = fields.Nested(User, dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    class Meta:
        model = Teacher
        fields = ("id", "user_id", "user", "created_at", "updated_at")
    @post_load
    def initiate_class(self, data_dict, many, partial):
        # pylint: disable=unused-argument,no-self-use
        return GeneralObject(**data_dict)

teacher_schema = TeacherSchema()
teachers_schema = TeacherSchema(many=True)