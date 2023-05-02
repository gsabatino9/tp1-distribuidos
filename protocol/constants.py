from struct import calcsize

EOF_MSG = bytes("EOF", 'utf-8')
HEADER = "!i"
LEN_HEADER = calcsize("!i")