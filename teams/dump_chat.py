#!/usr/bin/python3

import argparse

from skpy import Skype
from time import sleep
from datetime import datetime, timedelta

parser = argparse.ArgumentParser("dump_chat")
parser.add_argument("chat_id", help="The (internal) ID of Teams chat to be dumped (e.g. 19:c34f5733a352420584c5ad0037948823@thread.v2)")
parser.add_argument("-t", "--token", help="An personal access JWT token (e.g. ey... )")
parser.add_argument("-u", "--user", help="user name (e.g. hans.mueller@foo.bar)")
args = parser.parse_args()

if args.token != None:
  print("token passed")
  sk = Skype()
  sk.conn.tokenFile="/root/.tokens"
  sk.conn.tokens["skype"] = args.token
  sk.conn.tokenExpiry["skype"] = datetime.now() + timedelta(hours=1)
  sk.conn.userId = args.user
  sk.conn.getRegToken()
  sk.conn.msgsHost='https://emea.ng.msg.teams.microsoft.com/v1'
  sk.conn.writeToken()
else:
  sk = Skype(tokenFile="/root/.tokens")

ch = sk.chats[args.chat_id]
print("<html><body>\n")
while True:
  ms = ch.getMsgs()
  if (not ms):
    break
  for m in ms:
    print("<h4>", m.imdisplayname, m.time, "</h4>\n<p>", m.content, "</p>\n")
  sleep(1)

print("</html></body>\n")
