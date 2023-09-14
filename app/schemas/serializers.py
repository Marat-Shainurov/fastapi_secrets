def serializerDict(s) -> dict:
    return {
        **{i: str(s[i]) for i in s if i == "_id"},
        **{i: s[i] for i in s if i != "_id"}
    }
