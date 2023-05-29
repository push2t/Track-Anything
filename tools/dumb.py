LAST_VIDEO_FN = None
def last_video_fn(path=None):
    global LAST_VIDEO_FN
    if path is None:
        if LAST_VIDEO_FN is None:
            raise ValueError("no last video set boss")
        return LAST_VIDEO_FN

    LAST_VIDEO_FN = path
    return LAST_VIDEO_FN
