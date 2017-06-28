"""
Use this module to save cookies to pickle file.

This is currently only an example, and you must either manually add your own
    cookies, or copy them using a tool, such as the Chrome extension EditThisCookie.
"""


cookies = [
    {
        "domain": str(),
        "expirationDate": int(),
        "hostOnly": False,
        "httpOnly": False,
        "name": str(),
        "path": str(),
        "sameSite": str(),
        "secure": False,
        "session": False,
        "storeId": str(),
        "value": str(),
        "id": int()
    },
]


import pickle
pickle.dump(load_cookies(), open("cookie.pkl", "wb"))
