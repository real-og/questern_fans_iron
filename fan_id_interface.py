
def get_fan_id(all_users) -> int:
    used_ids = {
        int(user["fan_id"])
        for user in all_users
        if str(user.get("fan_id", "")).isdigit()
    }

    new_fan_id = 1

    while new_fan_id in used_ids:
        new_fan_id += 1

    return new_fan_id


def get_event_id(all_users, needed_event) -> int:
    used_ids = {
        int(user[needed_event])
        for user in all_users
        if str(user.get(needed_event, "")).isdigit()
    }

    new_event_id = 1

    while new_event_id in used_ids:
        new_event_id += 1

    return new_event_id