from datetime import datetime, timezone, timedelta

VN_TZ = timezone(timedelta(hours=7))

def now_vn() -> datetime:
    """
    trả về thời gian hiện tại ở Việt Nam

    Returns:
        datetime: _description_
    """
    return datetime.now(VN_TZ)

def now_vn_str(fmt = '%Y-%m-%d %H:%M:%S') -> str:
    """
    trả về thời gian dưới dạng str để lưu vào db

    Returns:
        str: _description_
    """
    return now_vn().strftime(fmt)