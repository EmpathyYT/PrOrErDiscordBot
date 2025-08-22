from constants import id_field_name, message_id_field_name, created_at_field_name, closed_alpha_field_name


class SubmittalObject:
    def __init__(self, submittal_id, message_id, created_at, is_closed_alpha):
        self.submittal_id = submittal_id
        self.message_id = message_id
        self.created_at = created_at
        self.is_closed_alpha = is_closed_alpha

    @classmethod
    def from_dict(cls, data: dict):
        if data is None:
            return None

        return cls(
            submittal_id=data.get(id_field_name),
            message_id=data.get(message_id_field_name),
            created_at=data.get(created_at_field_name),
            is_closed_alpha=data.get(closed_alpha_field_name, False)
        )

    def __repr__(self):
        return (f"SubmittalObject(submittal_id={self.submittal_id}, "
                f"message_id={self.message_id}, created_at={self.created_at})")
