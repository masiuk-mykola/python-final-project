from box import Box

patterns = Box(
    {
        "phone": r"^\+?[\d\s\-\(\)]{10,20}$",
        "email": r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
    }
)
