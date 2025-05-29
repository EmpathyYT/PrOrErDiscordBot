from constants import id_field_name, message_id_field_name, created_at_field_name


class SubmittalObject:
    def __init__(self, submittal_id, message_id, created_at):
        self.submittal_id = submittal_id
        self.message_id = message_id
        self.created_at = created_at

    @classmethod
    def from_dict(cls, data):
        if data is None:
            return None

        return cls(
            submittal_id=data.get(id_field_name),
            message_id=data.get(message_id_field_name),
            created_at=data.get(created_at_field_name)
        )

    def __repr__(self):
        return (f"SubmittalObject(submittal_id={self.submittal_id}, "
                f"message_id={self.message_id}, created_at={self.created_at})")
