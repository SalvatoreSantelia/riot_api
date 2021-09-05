from pescriot import *
from googleApi import *
from cassioLib import *

foglio = clonaFoglio("tutorial", nome_clonato="fallensalvo_game")
rows = makeRowsOfMatch("5416930262")
appendiRigheFoglio("fallensalvo_game", rows)
