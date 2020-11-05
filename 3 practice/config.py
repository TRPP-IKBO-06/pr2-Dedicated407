import sys
"""
let makeUser = \(user : Text) ->
      let home        = "/home/${user}"
      let privateKey  = "${home}/.ssh/id_ed25519"
      let publicKey   = "${privateKey}.pub"
      in  { home = home
          , privateKey = privateKey
          , publicKey  = publicKey
          }
    { - Add another user to this list - }
in  [ makeUser "Ilya"
    , makeUser "Maxim"
    ]
"""


def make_user(user: dict) -> dict:
    if type(user) is not str:
        print("ERROR: wrong type for a user", repr(user))
        sys.exit(1)
    home = f"/home/{user}"
    privateKey = f"{home}/.ssh/id_ed25519"
    publicKey = f"{privateKey}.pub"
    return dict(home=home, privateKey=privateKey, publicKey=publicKey)


data = [
    make_user("Ilya"),
    make_user("Maxim")
]