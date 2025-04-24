def get_bot_reply(message):
    msg = message.lower()
    if "job" in msg:
        return "We currently have openings in AI, Frontend, and Backend Development."
    elif "resume" in msg:
        return "Ensure your resume is clean, structured, and focused on the role."
    elif "interview" in msg:
        return "Prepare for common interview questions and be confident!"
    else:
        return "I can assist with job roles, resume tips, and interview guidance."
