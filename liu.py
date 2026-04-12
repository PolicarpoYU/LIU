import os
import unicodedata
import re
import json

ALIAS_BD=[
    # EMOGIS EQUIVALENTES:
    # RELOGIO
    ["⌚","⏱️","*⌚","*⏱️🤚"],
    ["⏰","⏱️","*⏰","*⏱️|☀️"],
    ["⏲️","⏱️","",""],
    ["🕰️","⏱️","",""],   
    ["⏱","⏱️","",""],
    # HORAS CHEIAS
    ["🕐","⏱️","🕐","*⏱️'(01:00H)'"],
    ["🕑","⏱️","🕑","*⏱️'(02:00H)'"],
    ["🕒","⏱️","🕒","*⏱️'(03:00H)'"],
    ["🕓","⏱️","🕓","*⏱️'(04:00H)'"],
    ["🕔","⏱️","🕔","*⏱️'(05:00H)'"],
    ["🕕","⏱️","🕕","*⏱️'(06:00H)'"],
    ["🕖","⏱️","🕖","*⏱️'(07:00H)'"],
    ["🕗","⏱️","🕗","*⏱️'(08:00H)'"],
    ["🕘","⏱️","🕘","*⏱️'(09:00H)'"],
    ["🕙","⏱️","🕙","*⏱️'(10:00H)'"],
    ["🕚","⏱️","🕚","*⏱️'(11:00H)'"],
    ["🕛","⏱️","🕛","*⏱️'(12:00H)'"],

    # MEIAS HORAS
    ["🕜","⏱️","🕜","*⏱️'(01:30H)'"],
    ["🕝","⏱️","🕝","*⏱️'(02:30H)'"],
    ["🕞","⏱️","🕞","*⏱️'(03:30H)'"],
    ["🕟","⏱️","🕟","*⏱️'(04:30H)'"],
    ["🕠","⏱️","🕠","*⏱️'(05:30H)'"],
    ["🕡","⏱️","🕡","*⏱️'(06:30H)'"],
    ["🕢","⏱️","🕢","*⏱️'(07:30H)'"],
    ["🕣","⏱️","🕣","*⏱️'(08:30H)'"],
    ["🕤","⏱️","🕤","*⏱️'(09:30H)'"],
    ["🕥","⏱️","🕥","*⏱️'(10:30H)'"],
    ["🕦","⏱️","🕦","*⏱️'(11:30H)'"],
    ["🕧","⏱️","🕧","*⏱️'(12:30H)'"],
    # SAPATO
    ["👞","👕🦶🏻","👞","👕🦶🏻"],
    ["👠","👕🦶🏻","👠","👕🦶🏻a"],
    ["👟","👕🦶🏻","👟","🙂👕🦶🏻"],
    ["🥾","👕🦶🏻","🥾","%👕🦶🏻"],
    # CARINHA → 🙂 
    ["😀","🙂","",""],  
    ["😃","🙂","",""],
    ["😄","🙂","",""],
    ["😁","🙂","",""],
    ["😆","🙂","",""],
    ["😅","🙂","",""],
    ["😂","🙂","",""],
    ["🤣","🙂","",""],
    ["😊","🙂","",""],
    ["😇","🙂","",""],
    ["🙂","🙂","",""],
    ["🙃","🙂","",""],
    ["😉","🙂","",""],
    ["😌","🙂","",""],
    ["😍","🙂","?😍","🙂 ((  _) *❤️ ))"],
    ["🥰","🙂","",""],
    ["😘","🙂","",""],
    ["😗","🙂","",""],
    ["😙","🙂","",""],
    ["😚","🙂","",""],
    ["🤗","🙂","",""],
    ["🤩","🙂","",""],
    ["🥳","🙂","",""],
    ["😎","🙂","",""],
    ["🤓","🙂","",""],
    ["🧐","🙂","",""],
    ["🥹","🙂","",""],
    # 🌲VEGETACAO 
    ["🌳","🌲","",""],
    ["🌴","🌲","",""],
    ["🎄","🌲","",""],
    ["🪾","🌲","*🪾","*🌲 ~🍀"],
    ["🌵","🌲","*🌵","*🌲 ~💧"],
    ["🌱","🌲","*🌱","v*🌲"],
    # Folha → 🍀
    ["🌿","🍀","",""],
    ["☘️","🍀","",""],
    # ÁRVORES → 🌲
    # flor 🌷
    ["🌾","🌷","",""],
    ["🌸","🌷","",""],
    ["🌹","🌷","🌹","🌷❤️"],
    ["🌺","🌷","",""],
    ["🌻","🌷","🌻","🌷☀️"],
    ["🌼","🌷","",""],
]

DB_ALIAS_NEW={
"🚗":[
    ["🚛","🚗📦"],
    ["🚜","🚗🌽"],
    ["🚂","🚗⚙️⚙️"],
    ["🚢","🚗💧⚙️"],
    ["🛶","🚗💧🪏"],
    ["⛵","🚗💧☁️"],
    ["✈️","🚗☁️"],
    ["🚁","🚗☁️⚙️"],
    ["🚠","🚗☁️🧵"],
    ["🚀","🚗🔥🌙"],
    ["🛸","🚗☀️"],
    ["🚴‍♂️","🚗🛞🛞"],
    ["🛼","🚗🛞🦶🏻"],
    ["🧑‍🦽","🚗🧍‍♂️🛞"],
    ["🏗️","🚗🧍‍♂️🏠"],
    ["🛷","🚗❄️🧸"],
],
"🌲":[
    ["🌳","🌲"],
    ["🌴","🌲☀️"],
    ["🎄","🌲🎅"],
    ["🪾","🌲~🍀"],
    ["🌵","🌲~💧"],
    ["🌱","v🌲"],
],
"🍀":[
    ["🌿","🍀"],
    ["☘️","🍀"],
],
"🌷":[
    ["🌾","🌷🌽"],
    ["🌸","🌷"],
    ["🌹","🌷❤️"],
    ["🌺","🌷"],
    ["🌻","🌷☀️"],
    ["🌼","🌷"],
],
"🐕":[ # TIPOS DE ANIMAIS
    ["🐄","🐕🥛"], # MAMÍFEROS
    ["🐓","🐕☁️"], # AVES E VOADORES
    ["🐟","🐕💧"], # PEIXES E ANIMAIS AQUÁTICOS
    ["🦎","🐕☀️"], # RÉPTEIS E ANFÍBIOS
    ["🐒","🐕🧑🏻‍🦱"], # PRIMATAS
    ["🐿️","🐕🌽"], # ROEDORES
    ["🐜","🐕<"], # INSETOS, ARACNÍDEOS E PEQUENOS ANIMAIS
],
"🐄":[ # MAMÍFEROS
    ["🐎","🐄🦵"],
    ["🐖","🐄🍴"],
    ["🐈","🐄👑🏠"],
    ["🐘","🐄💪"],
    ["🦏","🐄💪⚙️"],
    ["🐑","🐄👕"],
    ["🦒","🐄👄🌲"],
    ["🦘","🐄🦵🦵"],
    ["🦁","🐄👑"],
    ["🐇","🐄🍀"],
    ["🦄","🐄🌈"],
    ["🦨","🐄❌👃"],
    ["🐂","🐄💪"],
    ["🐃","🐄💧💪"],
    ["🦬","🐄💪🌲"],
    ["🫎","🐄🌲👑"],
    ["🫏","🐄🏠🦵"],
    ["🦌","🐄🌲"],
    ["🐅","🐄👑⚔️"],
    ["🐆","🐄👑🦵"],
    ["🦛","🐄💧💪"],
    ["🐺","🐄🌙"],
    ["🦊","🐄👑👄"],
    ["🦝","🐄🏠🤚"],
    ["🐻","🐄💪🏠"],
    ["🐼","🐄🌲⚫"],
    ["🐨","🐄🌲🌙"],
    ["🦥","🐄⌛🌲"],
    ["🦦","🐄💧🤚"],
    ["🦫","🐄🪏💧"],
    ["🦡","🐄🌲🪏"],
    ["🐪","🐄☀️☀️"],
    ["🐫","🐄☀️☀️☀️"],
    ["🦙","🐄👕👑"],
],
"🐓":[ # AVES E VOADORES
    ["🐥","🐓👶"],
    ["🦅","🐓☁️"],
    ["🦆","🐓☁️💧"],
    ["🦤","🐓☁️❌"],
    ["🐔","🐓🏠"],
    ["🦃","🐓🎉"],
    ["🐧","🐓❄️"],
    ["🕊️","🐓☮️"],
    ["🦢","🐓💧👑"],
    ["🦉","🐓🌙👁️"],
    ["🦚","🐓🌈"],
    ["🦜","🐓🔈🌈"],
    ["🪶","🐓👕"],
    ["🪽","🐓☁️"],
    ["🐦‍⬛","🐓⚫"],
    ["🪿","🐓💧🏠"],
    ["🐦‍🔥","🐓🔥"],
    ["🦇","🐓🌙"],
],
"🐟":[ # PEIXES E ANIMAIS AQUÁTICOS
    ["🐬","🐟🧑🏻‍🦱"],
    ["🐳","🐟💪"],
    ["🐋","🐟💪"],
    ["🦭","🐟🏠"],
    ["🐠","🐟🌈"],
    ["🐡","🐟⚙️"],
    ["🦈","🐟⚔️"],
    ["🐙","🐟🤚🤚"],
    ["🪼","🐟☁️💧"],
    ["🪸","🐟🌷"],
    ["🦞","🐟⚙️"],
    ["🦀","🐟🤚"],
    ["🦐","🐟🍴"],
],
"🦎":[ # RÉPTEIS E ANFÍBIOS
    ["🐢","🦎🏠"],
    ["🐍","🦎🦶🏻"],
    ["🐊","🦎💧⚔️"],
    ["🐸","🦎💧🔈"],
    ["🦖","🦎💪⌛"],
    ["🦕","🦎🌲⌛"],
],
"🐒":[ # MACACOS
    ["🐵","🎭*🐒"],
    ["🙈","*🐒 ~👁️"],
    ["*🙉","*🐒 ~👂"],
    ["🙊","*🐒 -👄"],
    ["🦍","*🐒💪"],
    ["🦧","*🐒🌲💪"],
],
"🐿️":[ # ROEDORES
    ["🐁","🐿️🌽"],
    ["🐀","🐿️🌽💪"],
    ["🐹","🐿️🌽🏠"],
],
"🐜":[ # INSETOS, ARACNÍDEOS E PEQUENOS ANIMAIS
    ["🕷️","🐜🕸️"],
    ["🦂","🐜💉"],
    ["🐝","🐜🍯"],
    ["🦗","🐜🔈"],
    ["🦟","🐜💧❤️"],
    ["🐞","🐜❤️"],
    ["🪲","🐜⚙️"],
    ["🪳","🐜🏠"],
    ["🪰","🐜💧🍴"],
    ["🦋","🐜🌷"],
    ["🐛","🐜🍀"],
    ["🪱","🐜🌎"],
    ["🐌","🐜⌛"],
],
}

def maiusc_LIU(DB):
    pares = {}
    for emoji in DB:
        lista = DB[emoji]
        if not isinstance(lista, list):
            continue
        for linha in lista:
            if not isinstance(linha, list):
                continue
            if len(linha) < 2:
                continue
            txt = str(linha[1]).strip()
            if not txt:
                continue
            # remove colchetes e parenteses, mas preserva conteúdo interno
            txt_limpo = txt.replace("[", "").replace("]", "")
            txt_limpo = txt_limpo.replace("(", "").replace(")", "")
            palavras = txt_limpo.split()
            for p in palavras:
                p = p.strip(" ,.;:!?\"'")
                if not p:
                    continue
                # ignora 1 letra só
                if len(p) == 1:
                    continue
                # ignora coisas com vírgula
                if "," in p:
                    continue
                chave = p.lower()
                if chave not in pares:
                    pares[chave] = set()
                pares[chave].add(p)
    TXT_maiusc = []
    for chave in sorted(pares.keys()):
        formas = pares[chave]
        # 1 forma só
        if len(formas) == 1:
            unica = list(formas)[0]
            # só guarda se tiver alguma maiúscula
            if unica != unica.lower():
                TXT_maiusc.append(unica)
        else:
            forma_low = None
            forma_up = None
            for f in formas:
                if len(f) == 1:
                    continue
                if "," in f:
                    continue
                if f == f.lower():
                    forma_low = f
                elif f[0].isupper() and f[1:] == f[1:].lower():
                    forma_up = f
            if forma_low and forma_up:
                TXT_maiusc.append(f"{forma_low}/{forma_up}")
            else:
                itens_validos = []
                for f in sorted(formas):
                    if len(f) == 1:
                        continue
                    if "," in f:
                        continue
                    itens_validos.append(f)
                if itens_validos:
                    TXT_maiusc.append("/".join(itens_validos))
    return TXT_maiusc

def maiusc_inicio_frase(txt):
    txt = txt.strip()
    if not txt:
        return txt
    return txt[0].upper() + txt[1:]

# =========================
# CARREGAR DB
# =========================
def load_db(FILE_NAME):
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME,"r", encoding="utf-8") as f:
            return True,json.load(f)
    return False,{}

# =========================
# SALVAR DB
# =========================
def save_db(FILE_NAME,DB,Forca_grava=True):
    if not Forca_grava: # se tiver arquivo nao sobreescreve
       if os.path.exists(FILE_NAME):     
          print(f"Arquivo:{FILE_NAME}, já existe: não gravou novamente")
          return 
    with open(FILE_NAME,"w", encoding="utf-8") as f:
        json.dump(DB, f, ensure_ascii=False, indent=2)
        print(f"Gravou:{FILE_NAME}")

# =========================
# IMPRIME RESUMI DA DB LIU
# =========================
def resumo_LIU(DB):
    def formata_titulo(txt):
        txt = str(txt).strip().lower()
        if not txt:
            return ""
        return txt[0].upper() + txt[1:]

    def pega_significados_base(emoji, lista):
        sig_emoji = ""
        sig_obj = ""
        if not isinstance(lista, list):
            return sig_emoji, sig_obj
        for linha in lista:
            if not isinstance(linha, list) or len(linha) < 2:
                continue
            chave = str(linha[0]).strip()
            valor = str(linha[1]).strip()
            if chave == emoji and not sig_emoji:
                sig_emoji = formata_titulo(valor)
            elif chave == "*" + emoji and not sig_obj:
                sig_obj = formata_titulo(valor)
            if sig_emoji and sig_obj:
                break
        return sig_emoji, sig_obj

    total_geral = 0
    resumo = []
    ct = 0

    for emoji in DB:
        lista = DB[emoji]
        qtd = len(lista) if isinstance(lista, list) else 0
        total_geral += qtd
        sig_emoji, sig_obj = pega_significados_base(emoji, lista)
        resumo.append((emoji, qtd, sig_emoji, sig_obj))

    resumo.sort(key=lambda x: x[1], reverse=True)

    print("=== RESUMO LIU (ORDENADO) ===")
    for emoji, qtd, sig_emoji, sig_obj in resumo:
        ct += 1
        txt_extra = ""
        if sig_emoji:
            txt_extra += f"{emoji} => {sig_emoji:>20}"
        if sig_obj:
            if txt_extra:
                txt_extra += f";  *{emoji} => {sig_obj}"
            else:
                txt_extra += f"*{emoji} => {sig_obj}"
        if txt_extra:
            print(f"{ct}: {txt_extra}  ({qtd})")
        else:
            print(f"{ct}: {emoji} => {qtd}")

    print("=============================")
    print(f"TOTAL => {ct} emogis básicos, {total_geral} palavras")

    ct = 1
    for emoji, qtd, sig_emoji, sig_obj in resumo:
        if emoji not in ["🔣", "⁉️"]:
            if ct % 16 == 1:
                print(f"\n# {ct:3}", end="")
            print(f"{emoji}", end="")
            ct += 1

# =========================
# LETRA MINUSCULA=> COMPATIBILIZA COM LIU 
# =========================
def lower(p,TXT_maiusc):
    if p in ["K","M","G","P","T"]:
        return p

    for termo in TXT_maiusc:
        if "/" in termo:
            a, b = termo.split("/")

            # caso exato
            if p == a:
                return a
            if p == b:
                return b

            # se veio tudo maiúsculo, assume forma da direita
            if p.isupper() and p.lower() == a.lower():
                return b

            # qualquer outro caso cai para a forma minúscula
            if p.lower() == a.lower():
                return a

        else:
            if p.lower() == termo.lower():
                return termo

    return p.lower()

# ============================================================
# NORMALIZAÇÃO
# ============================================================
def normaliza_simbolo(s):
    if not s:
        return s

    # normalização unicode padrão
    s = unicodedata.normalize("NFC", s)

    # remove duplicação de variation selector (emoji bug)
    while "️️" in s:
        s = s.replace("️️", "️")

    # remove espaços indevidos dentro de símbolo
    s = s.strip()
    s = s.replace(" ", "")

    return s

# ============================================================
# IDENTIFICA GRUPO (EMOJI PRINCIPAL)
# ============================================================
def pega_grupo_simbolo(simb, DBini):
    for c in simb:
        if c in DBini:
            return c
    return None

# ============================================================
# BUSCA OTIMIZADA NA DB
# ============================================================
def busca_linha_DB(simb, DBini, debug=False):

    simb = normaliza_simbolo(simb)

    if debug:
        print(f"\n🔍 BUSCANDO: [{simb}] len={len(simb)}")
        print("HEX:", [hex(ord(c)) for c in simb])

    grupo = pega_grupo_simbolo(simb, DBini)

    candidatos = []

    if grupo:
        if debug: print(f"🔎 Grupo: {grupo}")
        candidatos += DBini.get(grupo, [])

    if "_" in simb or "=" in simb:
        if debug: print("🔎 Grupo: 🅰️")
        candidatos += DBini.get("🅰️", [])

    if not grupo:
        if debug: print("🔎 Grupo: 🔣")
        candidatos += DBini.get("🔣", [])

    # BUSCA DETALHADA
    for linha_DB in candidatos:
        SDB = normaliza_simbolo(linha_DB[0])

        if 0:# debug:
            print(f"COMPARA: [{SDB}] vs [{simb}]")
            print("HEX DB:", [hex(ord(c)) for c in SDB])

        if SDB == simb:
            if debug: print("✅ ACHOU:", linha_DB)
            return linha_DB

    # fallback total
    if debug: print("⚠️ fallback geral")

    for g in DBini:
        for linha_DB in DBini[g]:
            SDB = normaliza_simbolo(linha_DB[0])

            if SDB == simb:
                if debug: print("✅ ACHOU fallback:", linha_DB)
                return linha_DB

    return None

# ============================================================
# TROCA ALIAS (VERSÃO FINAL CORRETA)
# ============================================================
def troca_alias(simb, ALIAS_BD):

    original = simb

    # 1️⃣ match exato
    for base, base_sub, filtro, sub in ALIAS_BD:
        if simb == base:
            return sub if sub else base_sub

    # 2️⃣ match com filtro
    for base, base_sub, filtro, sub in ALIAS_BD:
        if filtro and simb == filtro:
            return sub

    # 3️⃣ substituição parcial
    for base, base_sub, filtro, sub in ALIAS_BD:
        if base in simb:
            simb = simb.replace(base, base_sub)

    return simb

# ============================================================
# EXTRAI DADOS DA LINHA DB
# ============================================================
def pega_dados(linha_DB):

    SIMB = linha_DB[0]
    TXT = linha_DB[1]
    EXTRA = linha_DB[2] if len(linha_DB) > 2 else ""

    # -----------------------------
    # TXT_PAD + EXT
    # -----------------------------
    partes = re.findall(r"\((.*?)\)", TXT)

    TXT_PAD = TXT.split(" (")[0]
    TXT_PAD = TXT_PAD.replace("[", "").replace("]", "").strip()

    TXT_EXT = None
    if len(partes) == 1:
        TXT_EXT = partes[0]
        if TXT_EXT:
           TXT_EXT = TXT_EXT.replace("[", "").replace("]", "").strip()

    # -----------------------------
    # EXPLICAÇÃO
    # -----------------------------
    explic = re.findall(r"\[(.*?)\]", EXTRA)
    TXT_EXPLIC = explic[0] if explic else None

    # -----------------------------
    # KEYS
    # -----------------------------
    chaves = re.findall(r"\((.*?)\)", EXTRA)

    LISTA_TXT_KEY = []

    if partes and chaves and len(partes) == len(chaves):
        for i in range(len(chaves)):
            LISTA_TXT_KEY.append((chaves[i], partes[i]))

    # -----------------------------
    # KEY principal { }
    # -----------------------------
    key_match = re.findall(r"\{(.*?)\}", EXTRA)
    KEY = key_match[0] if key_match else None

    return SIMB, TXT_PAD, TXT_EXT, TXT_EXPLIC, LISTA_TXT_KEY, KEY

# ============================================================
# APLICA CHAVES
# ============================================================
def aplica_keys(LISTA_TXT_KEY, Lista_Key, base_atual, usa_pessoa=True, usa_posse=False, debug=False):

    PESSOA_KEYS = ["1ps", "2ps", "3ps", "1pp", "2pp", "3pp"]
    POSSE_KEYS  = ["1&s", "2&s", "3&s", "1&p", "2&p", "3&p"]

    MAPA_POSSE_PARA_PESSOA = {
        "1&s": "1ps",
        "2&s": "2ps",
        "3&s": "3ps",
        "1&p": "1pp",
        "2&p": "2pp",
        "3&p": "3pp"
    }

    if not LISTA_TXT_KEY or not Lista_Key:
        return base_atual, False

    lista_norm = [str(x).strip() for x in Lista_Key]

    if debug:
        print(">> Aplicando KEY",
              "(pessoa)" if usa_pessoa else "(posse)" if usa_posse else "(geral)")
        print("Lista_Key normalizada:", lista_norm)

    pessoa_prioritaria = None

    # -----------------------------
    # MODO 1: pessoa verbal normal
    # -----------------------------
    if usa_pessoa:
        for k in lista_norm:
            if k in PESSOA_KEYS:
                pessoa_prioritaria = k
                break

    # -----------------------------
    # MODO 2: posse -> pessoa verbal
    # -----------------------------
    elif usa_posse:
        for k in lista_norm:
            if k in POSSE_KEYS:
                pessoa_prioritaria = MAPA_POSSE_PARA_PESSOA[k]
                break

    if debug and (usa_pessoa or usa_posse):
        print("pessoa_prioritaria:", pessoa_prioritaria)

    for k, val in LISTA_TXT_KEY:

        if isinstance(k, str):
            chaves = [x.strip() for x in k.replace(",", " ").split() if x.strip()]
        else:
            chaves = [str(k).strip()]

        if usa_pessoa or usa_posse:
            chaves_filtradas = [c for c in chaves if c in PESSOA_KEYS]
        else:
            chaves_filtradas = [c for c in chaves if c not in PESSOA_KEYS and c not in POSSE_KEYS]

        if not chaves_filtradas:
            continue

        if (usa_pessoa or usa_posse) and pessoa_prioritaria is not None:
            if pessoa_prioritaria not in chaves_filtradas:
                if debug:
                    print(f"  ignorando grupo {chaves_filtradas} porque não contém {pessoa_prioritaria}")
                continue

        if debug:
            print(f"  comparando grupo {chaves_filtradas} com Lista_Key={lista_norm}")

        contador = 0
        for c in chaves_filtradas:
            if c in lista_norm or c == pessoa_prioritaria:
                contador += 1

        if debug:
            print(f"  contador={contador} / tamanho={len(chaves_filtradas)}")

        if contador == len(chaves_filtradas):
            if debug:
                print("  ✅ MATCH TOTAL →", val)
            return val, True

    if debug:
        print("  ❌ Nenhuma KEY aplicada")

    return base_atual, False

# ============================================================
# RETORNA PALAVRA FINAL
# ============================================================
def retorna_palavra(linha_DB, usa_PAD=True, usa_EXT=False, usa_EXPLIC=False, Usa_Key=True, Lista_Key=None, debug=False):
#    debug=True
    if Lista_Key is None:
        Lista_Key = []

    SIMB, TXT_PAD, TXT_EXT, TXT_EXPLIC, LISTA_TXT_KEY, KEY = pega_dados(linha_DB)

    if debug:
        print("\n==============================")
        print("SIMB:", SIMB)
        print("TXT_PAD:", TXT_PAD)
        print("LISTA_TXT_KEY:", LISTA_TXT_KEY)
        print("Lista_Key ENTRADA:", Lista_Key)

    base = TXT_PAD

    # =========================
    # aplica KEY (DEBUG REAL)
    # =========================

    if Usa_Key and LISTA_TXT_KEY and Lista_Key:

        # 1ª passada: tenta pessoa verbal primeiro
        base, achou = aplica_keys(
            LISTA_TXT_KEY,
            Lista_Key,
            base,
            usa_pessoa=True,
            usa_posse=False,
            debug=debug
        )

     # 2ª passada: tenta pessoa posse primeiro
        if not achou:
          base, achou = aplica_keys(
            LISTA_TXT_KEY,
            Lista_Key,
            base,
            usa_pessoa=False,
            usa_posse= True ,
            debug=debug
        )

        # 3ª passada: se não achou, tenta o resto
        if not achou:
            base, achou = aplica_keys(
                LISTA_TXT_KEY,
                Lista_Key,
                base,
                usa_pessoa=False,
                usa_posse=False,
                debug=debug
            )

   
    # =========================
    # adiciona KEY nova
    # =========================
    KEY1=""
    if ':' in SIMB:
       KEY1+=" num_plu "
       if debug: print("KEY >> num_plu")
    if 'a' in SIMB: 
       KEY1+=" gen_fem "
       if debug: print("KEY >> gen_fem")
    if 'o' in SIMB: 
       KEY1+=" gen_masc "
       if debug: print("KEY >> gen_masc")
    if KEY:
       KEY+=KEY1
    else:
      if len(KEY1)>0:
         KEY=KEY1       

    if KEY:
        chaves = [x.strip() for x in KEY.strip().split() if x.strip()]

        for k in chaves:

            # gênero é excludente
            if k == "gen_fem":
                if "gen_masc" in Lista_Key:
                    Lista_Key.remove("gen_masc")
                    if debug:
                        print(">> KEY removida: gen_masc")
            elif k == "gen_masc":
                if "gen_fem" in Lista_Key:
                    Lista_Key.remove("gen_fem")
                    if debug:
                        print(">> KEY removida: gen_fem")

            if k not in Lista_Key:
                Lista_Key.append(k)
                if debug:
                    print(">> KEY adicionada:", k)

    if debug:
        print("Lista_Key FINAL:", Lista_Key)
        print("BASE FINAL:", base)

    # =========================
    # montagem
    # =========================
    if usa_PAD and not usa_EXT and not usa_EXPLIC:
        TXT_OUT = base

    elif usa_PAD and usa_EXT and not usa_EXPLIC:
        TXT_OUT = f"{base} ({TXT_EXT})" if TXT_EXT else base

    elif not usa_PAD and usa_EXT:
        TXT_OUT = TXT_EXT if TXT_EXT else base

    elif usa_PAD and usa_EXT and usa_EXPLIC:
        partes = []
        if TXT_EXT: partes.append(TXT_EXT)
        if TXT_EXPLIC: partes.append(TXT_EXPLIC)
        TXT_OUT = f"{base} ({'/'.join(partes)})"

    elif usa_PAD and not usa_EXT and usa_EXPLIC:
        TXT_OUT = f"{base} ({TXT_EXPLIC})" if TXT_EXPLIC else base

    elif not usa_PAD and not usa_EXT and usa_EXPLIC:
        TXT_OUT = TXT_EXPLIC if TXT_EXPLIC else base

    else:
        TXT_OUT = base

    if debug:
        print("TXT_OUT:", TXT_OUT)
        print("==============================")

    return TXT_OUT, Lista_Key

# ============================================================
# EXTRAI MEMOGIS
# ============================================================
def extrai_emojis(s):
    return [c for c in s if ord(c) > 10000]

# ============================================================
# BUSCA SIMBOLO LIU
# ============================================================
def busca_simbolo(simb, DB, debug=False):

    simb = normaliza_simbolo(simb)

    # --------------------------------
    # seletor p/s
    # p = fora de []
    # s = dentro de []
    # --------------------------------
    modo_ps = ""
    simb_busca = simb

    if len(simb_busca) > 1 and simb_busca[0] in ["p", "s"]:
        modo_ps = simb_busca[0]
        simb_busca = simb_busca[1:]

    # 1️⃣ grupo principal
    grupos = []

    emojis = extrai_emojis(simb_busca)

    if "_" in simb_busca:
        grupos.append("⛓️")

    if not emojis:
        grupos.append("🔣")
    else:
        grupos.append(emojis[-1])

    # 2️⃣ adicionar outros emojis como fallback
    for e in emojis:
        if e not in grupos:
            grupos.append(e)

    def ajusta_linha_ps(linha):
        if not modo_ps:
            return linha

        nova = list(linha)
        txt = str(nova[1])

        txt_sem_paren = re.sub(r"\(.*?\)", "", txt).strip()

        if modo_ps == "s":
            partes = re.findall(r"\[(.*?)\]", txt_sem_paren)
            txt_novo = " ".join(partes).strip()
        else:  # modo_ps == "p"
            txt_novo = re.sub(r"\[.*?\]", "", txt_sem_paren).strip()

        txt_novo = txt_novo.replace("[", "").replace("]", "").strip()

        nova[1] = txt_novo
        return nova

    # 3️⃣ busca por grupo
    for g in grupos:
        if g in DB:
            for linha in DB[g]:
                if normaliza_simbolo(linha[0]) == simb_busca:
                    if debug:
                        print("✅ ACHOU EM GRUPO:", g)
                    return ajusta_linha_ps(linha)

    # 4️⃣ fallback TOTAL
    if debug:
        print("⚠️ BUSCA GLOBAL")

    for g in DB:
        for linha in DB[g]:
            if normaliza_simbolo(linha[0]) == simb_busca:
                if debug:
                    print("✅ ACHOU GLOBAL:", g)
                return ajusta_linha_ps(linha)

    return None

# ============================================================
# TRATA PALAVRAS GERAL
# ============================================================
def trata_geral(TXT_maiusc,simb, DBini, DB_COMP, Lista_Key, debug=False):
    if debug:
        print("\n🔧 trata_geral:", simb)
        print("Lista_Key entrada:", Lista_Key)
    simb = lower(simb,TXT_maiusc)
    # -------------------------
    # 1. prefixo (~ # *)
    # -------------------------
    prefixo = ""
    if simb.startswith(("~", "#", "*")):
        prefixo = simb[0]
        simb = simb[1:]

    # -------------------------
    # 2. sufixos (a o :)
    # -------------------------
    sufixos = []
    base = simb

    while base and base[-1] in [":", "a", "o"]:
        sufixos.append(base[-1])
        base = base[:-1]

    sufixos = sufixos[::-1]

    if debug:
        print("prefixo:", prefixo)
        print("base:", base)
        print("sufixos:", sufixos)

    # -------------------------
    # 3. busca símbolo
    # -------------------------
    simbolo_full = prefixo + base if prefixo else base

    linha = busca_simbolo(simbolo_full, DBini, debug)

    usou_base = False

    if not linha:
        linha = busca_simbolo(base, DBini, debug)
        usou_base = True

    if not linha:
        if debug: print("❌ não achou base")
        return None, Lista_Key

    if debug:
        print("linha encontrada:", linha)

    # -------------------------
    # 🔥 USA retorna_palavra (igual verbo)
    # -------------------------
    palavra, Lista_Key = retorna_palavra(
        linha,
        usa_PAD=True,
        usa_EXT=False,
        usa_EXPLIC=False,
        Usa_Key=True,
        Lista_Key=Lista_Key
    )

    if debug:
        print("BASE:", palavra)
        print("Lista_Key após base:", Lista_Key)

    # -------------------------
    # 4. aplica prefixo (fallback)
    # -------------------------
    if usou_base and prefixo:
        for k, desc in DB_COMP:
            if k == prefixo:
                palavra = desc + " " + palavra
                break

    # -------------------------
    # 5. aplica sufixos + atualiza KEY
    # -------------------------
    mods = []

    for s in sufixos:

        for k, desc in DB_COMP:
            if k == s:

                mods.append(desc)

                # 🔥 ATUALIZA LISTA_KEY
                if s == ":" and "num_plu" not in Lista_Key:
                    Lista_Key.append("num_plu")

                if s == "a" and " gen_fem" not in Lista_Key:
                    Lista_Key.append(" gen_fem")

                break

    # -------------------------
    # 6. junta modificadores
    # -------------------------
    if mods:

        mods_limpos = []

        for m in mods:
            m = m.strip()
            if m.startswith("(") and m.endswith(")"):
                m = m[1:-1]
            mods_limpos.append(m)

        palavra += " (" + ", ".join(mods_limpos) + ")"

    if debug:
        print("RESULTADO FINAL:", palavra)
        print("Lista_Key FINAL:", Lista_Key)

    return palavra, Lista_Key

# ============================================================
# TRARA VERBOS
# ============================================================
def trata_verbo(TXT_maiusc,simb, DBini, DB_COMP, Lista_Key, debug=False):

    if debug:
        print("\n🔧 trata_verbo:", simb)
        print("Lista_Key recebida:", Lista_Key)

    simb = lower(simb,TXT_maiusc)

    # evita tratar !!
    if simb == "!!":
        return None, Lista_Key

    # -------------------------
    # prefixo (~ # *)
    # -------------------------
    prefixo = ""
    if simb[0] in ["~", "#", "*"]:
        prefixo = simb[0]
        simb = simb[1:]

    # -------------------------
    # sufixo (tempo)
    # -------------------------
    sufixo = ""
    if simb[-1] in ["^", "v", "=", "!", "?"]:
        sufixo = simb[-1]
        base = simb[:-1]
    else:
        base = simb

    if debug:
        print("prefixo:", prefixo)
        print("base:", base)
        print("sufixo:", sufixo)

    # -------------------------
    # tenta achar base completa
    # -------------------------
    linha_base = busca_simbolo(prefixo + base, DBini, debug)

    usou_base = False

    if not linha_base:
        linha_base = busca_simbolo(base, DBini, debug)
        usou_base = True

    if not linha_base:
        if debug: print("❌ verbo não encontrado")
        return None, Lista_Key

    if debug:
        print("linha encontrada:", linha_base)

    # -------------------------
    # 🔥 AQUI É O PONTO CRÍTICO
    # usa retorna_palavra com Lista_Key
    # -------------------------
    TXT_BASE, _ = retorna_palavra(
        linha_base,
        usa_PAD=True,
        usa_EXT=False,
        usa_EXPLIC=False,
        Usa_Key=True,
        Lista_Key=Lista_Key.copy()
    )

    if debug:
        print("VERBO CONJUGADO:", TXT_BASE)

    # -------------------------
    # aplica tempo
    # -------------------------
    for k, desc in DB_COMP:
        if k == sufixo:
            TXT_BASE = f"{TXT_BASE} {desc}"
            break

    # -------------------------
    # aplica prefixo (se fallback)
    # -------------------------
    if usou_base and prefixo:
        for k, desc in DB_COMP:
            if k == prefixo:
                TXT_BASE = f"{desc} {TXT_BASE}"
                break

    if debug:
        print("RESULTADO FINAL:", TXT_BASE)

    return TXT_BASE, Lista_Key

# ============================================================
# CONVERSOR LIU => TXT UMA LINHA
# ============================================================
def converte_LIU_TXT_base(TXT_maiusc,linha_LIU, DBini, ALIAS_BD,
                     usa_PAD=True, usa_EXT=False,
                     usa_EXPLIC=False, Usa_Key=True,
                     debug=False, debugw=False):

    linha_LIU=pre_processa_LIU(linha_LIU)
    DB_COMP = DBini.get("⁉️", [])
    if debug: print("\n======= LUI => TXT ==============")
    if debug: print("ENTRADA:", linha_LIU)
    # -----------------------------
    # 1. tokenização
    # -----------------------------
    tokens = linha_LIU.split()
    if debug: print("TOKENS:", tokens)
    # -----------------------------
    # 2. alias
    # -----------------------------
    tokens_alias = []
    for t in tokens:
        novo = troca_alias(t, ALIAS_BD)
        novo = normaliza_simbolo(novo)
        if debug and novo != t:
            print(f"ALIAS: {t} => {novo}")
        tokens_alias.append(novo)
    if debug: print("TOKENS_APOS_ALIAS:", tokens_alias)
    # =========================================================
    # 🔥 PASSO 0 — COLETA DE KEY
    # =========================================================
    Lista_Key = []
    if debug: print("\n==== PASSO 0: COLETA KEY ====")
    for simb in tokens_alias:
        simb = normaliza_simbolo(simb)
        linha_DB = busca_linha_DB(simb, DBini, debug)
        if linha_DB:
            _, Lista_Key = retorna_palavra(
                linha_DB,
                usa_PAD=True,
                usa_EXT=False,
                usa_EXPLIC=False,
                Usa_Key=True,
                Lista_Key=Lista_Key,
                debug=debugw
            )
        else:
            # tenta verbo
            verbo, Lista_Key = trata_verbo(TXT_maiusc,simb, DBini, DB_COMP, Lista_Key, debug)
            if not verbo:
                # tenta geral
                _, Lista_Key = trata_geral(TXT_maiusc,simb, DBini, DB_COMP, Lista_Key, debug)
    if debug:
        print("Lista_Key FINAL PASSO 0:", Lista_Key)
    # =========================================================
    # 🔥 PASSO 1 — TRADUÇÃO FINAL
    # =========================================================
    if debug: print("\n==== PASSO 1: TRADUÇÃO ====")
    saida = []
    for simb in tokens_alias:
        simb = normaliza_simbolo(simb)
        if debug: print("\n--- PROCESSANDO:", simb)
        linha_DB = busca_linha_DB(simb, DBini, debug)
        if linha_DB:
            TXT_OUT, _ = retorna_palavra(
                linha_DB,
                usa_PAD=usa_PAD,
                usa_EXT=usa_EXT,
                usa_EXPLIC=usa_EXPLIC,
                Usa_Key=Usa_Key,
                Lista_Key=Lista_Key.copy(),  # 🔥 IMPORTANTE
                debug=debugw
            )
            if debug:
                print("TXT:", TXT_OUT)
            saida.append(TXT_OUT)
        else:
            # tenta verbo
            verbo, _ = trata_verbo(TXT_maiusc,simb, DBini, DB_COMP, Lista_Key.copy(), debug)
            if verbo:
                if debug: print("✔ TRATA_VERBO:", verbo)
                saida.append(verbo)
            else:
                geral, _ = trata_geral(TXT_maiusc,simb, DBini, DB_COMP, Lista_Key.copy(), debug)
                if geral:
                    saida.append(geral)
                else:
                    saida.append(simb)
    # -----------------------------
    # 3. saída final
    # -----------------------------
    linha_TXT = " ".join(str(x) for x in saida)
    linha_TXT = linha_TXT.replace("'", "")
    if debug:
        print("\nSAIDA FINAL:", linha_TXT)
        print("==============================\n")
    return linha_TXT


# ============================================================
# CONVERSOR LIU => TXT VARIAS LINHAS
# ============================================================
def converte_LIU_TXT(TXT_maiusc,linha_LIU, DBini, ALIAS_BD,
                     usa_PAD=True, usa_EXT=False,
                     usa_EXPLIC=False, Usa_Key=True,
                     debug=False, debugw=False):

    if linha_LIU is None:
        return ""
    linha = str(linha_LIU)
    linha = pre_processa_LIU(linha)
    tokens = linha.split()
    # separadores que encerram frase
    FIM_FRASE = [".", "?",":", "!", "_n"]
    blocos = []
    atual = []
    for t in tokens:
        atual.append(t)
        if t in FIM_FRASE:
            blocos.append(" ".join(atual).strip())
            atual = []
    if atual:
        blocos.append(" ".join(atual).strip())
    if debug:
        print("\n======= LIU => TXT POR FRASES =======")
        print("BLOCOS:", blocos)
    saida_blocos = []
    for i, bloco in enumerate(blocos):
        if not bloco:
            continue
        # normaliza final duplicado
        bloco = bloco.replace("!!", "!")
        bloco = bloco.replace("??", "?")
        txt_bloco = converte_LIU_TXT_base(
            TXT_maiusc,
            bloco,
            DBini,
            ALIAS_BD,
            usa_PAD=usa_PAD,
            usa_EXT=usa_EXT,
            usa_EXPLIC=usa_EXPLIC,
            Usa_Key=Usa_Key,
            debug=debug,
            debugw=debugw
        )
        txt_bloco = str(txt_bloco).strip()
        txt_bloco= maiusc_inicio_frase(txt_bloco)
        saida_blocos.append(txt_bloco)
        if debug:
            print(f"BLOCO {i}: [{bloco}] => [{txt_bloco}]")
    linha_TXT = " ".join(saida_blocos)
    # limpa espaços antes de pontuação
    linha_TXT = re.sub(r"\s+([,.;:!?])", r"\1", linha_TXT)
    linha_TXT = re.sub(r"\s{2,}", " ", linha_TXT).strip()
    linha_TXT=fim_processa_txt(linha_TXT)
    if debug:
        print("SAIDA FINAL:", linha_TXT)
        print("=====================================\n")
    return linha_TXT


# ============================================================
# POS PROCESSAMENTO DE ALIAS 
# ============================================================
def pos_processa(linha_LIU, ALIAS_BD,debug=False):
    if debug: print("=========> POS PROCESSAMENTO:")
    # 1. normaliza espaços
    # -------------------------
    linha = " ".join(linha_LIU.split())
    linhaorig=linha
    # -------------------------
    # 3. junta genero/plural
    # -------------------------
    linha = re.sub(r"(\S)\s+([aox:])\b", r"\1\2", linha)
    if debug: 
       if (linhaorig!=linha):
          linhaorig=linha
          print(f"passo 3:{linha}")
    # -------------------------
    # 4. junta operadores (_ # *)
    # regra:
    # _ 🙂   → _🙂
    # # ❤️   → #❤️
    # * 🐕   → *🐕
    # -------------------------
    tokens = linha.split()
    nova = []
    i = 0
    OPERADORES = ["_", "#", "*"]
    while i < len(tokens):
        t = tokens[i]
        if i + 1 < len(tokens):
            prox = tokens[i + 1]
            operador_isolado = t in OPERADORES
            prox_simples = len(prox) > 0 and prox[0] not in OPERADORES + ["^", "v", "=", "?", "!"]
            if operador_isolado and prox_simples:
                if debug:
                    print(f"unindo t{t} + prox{prox} = {t + prox}")
                t = t + prox
                i += 1
        nova.append(t)
        i += 1
    linha = " ".join(nova)
    if debug:
        if linhaorig != linha:
            linhaorig = linha
            print(f"passo 4:{linha}")
    # -------------------------
    # 5. junta sufixos de verbo
    # SOMENTE se estiver SOLTO
    # regra:
    # !❤️  =   → junta
    # !❤️ =🙂 → NÃO junta
    # -------------------------
    tokens = linha.split()
    nova = []
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if i + 1 < len(tokens):
            prox = tokens[i + 1]
            sufixo_isolado = prox in ["^", "v", "=", "?", "!"]
            token_verbal = t.startswith("!")
            if token_verbal and sufixo_isolado:
                if debug: print(f"unindo  t{t} + prox{prox}= { t + prox}")
                t = t + prox
                i += 1
        nova.append(t)
        i += 1
    linha = " ".join(nova)
    # -------------------------
    # 6. aplica alias (forma curta)
    # -------------------------
    for item in ALIAS_BD:
        if len(item) < 4:
            continue
        curto = item[2]
        longo = item[3]
        if curto and longo:
            linha = linha.replace(longo, curto)
    return linha


# ============================================================
# LIMPRA FRASE
# ============================================================
def limpa_frase(TXT_maiusc,frase):
    STOPWORDS={"de","do","da","dos","das","no","na","nos","nas","o","a","os","as"}
    palavras_orig=frase.split()
    palavras_low=[]
    for i in range(len(palavras_orig)):
       palavras_low.append(lower(palavras_orig[i],TXT_maiusc)) 
    if len(palavras_orig)==1:
        return palavras_orig[0]
    i=0
    while i<len(palavras_low) and palavras_low[i] in STOPWORDS:
        i+=1
    palavras_filtradas=palavras_orig[i:]
    if not palavras_filtradas:
        palavras_filtradas=palavras_orig
    return " ".join(palavras_filtradas)

# =========================
# EXTRAI PALAVRAS DA COLUNA 2
# =========================
def extrai_palavras(TXT_maiusc,txt):
    resultados = []
    txt = txt.strip()
    # -------------------------
    # separa parte externa e interna
    # -------------------------
    partes_parenteses = re.findall(r"\((.*?)\)", txt)
    # remove parenteses do texto principal
    texto_base = re.sub(r"\(.*?\)", "", txt).strip()
    # 1. PROCESSA BASE
    if texto_base:
        base_limpa = limpa_frase(TXT_maiusc,texto_base)
        if base_limpa:
            resultados.append(base_limpa)
    # 2. PROCESSA PARENTESES
    for p in partes_parenteses:
        p = p.strip()
        if not p:
            continue
        p_limpo = limpa_frase(TXT_maiusc,p)
        if p_limpo:
            resultados.append(p_limpo)
    # remove duplicados
    resultados = list(dict.fromkeys(resultados))
    return resultados

# =========================
# CRIA DB_TXT
# =========================
def cria_DB_TXT(TXT_maiusc,DBini, FILE_NAME_TXT, reinicia=False):
    if not reinicia:
        ok, db = load_db(FILE_NAME_TXT)
        if ok:
            print("DB_TXT carregado de arquivo.")
            return db
    print("Gerando DB_TXT estruturado...")
    DB_TXT={}
    STOP={"de","do","da","dos","das","no","na","nos","nas","o","a","os","as"}
    def limpa_txt(s):
        palavras=s.strip().split()
        tam = len(palavras)
        palavra_out=[]
        for i in range(tam):
            usa=True
            if tam>1 and i==0:
               if lower(palavras[i],TXT_maiusc) in STOP:
                  usa=False 
            if  usa:       
              palavra_out.append(palavras[i])
        return " ".join(palavra_out)

    def extrai_pares(simb, txt, extra):
        partes = re.findall(r"\((.*?)\)", txt)

        # texto completo preservando ordem original
        texto_sem_paren = re.sub(r"\(.*?\)", "", txt).strip()
        texto_completo = texto_sem_paren.replace("[", "").replace("]", "")
        texto_completo = limpa_txt(texto_completo)

        # parte base = fora de [ ]
        base_bruta = re.sub(r"\[.*?\]", "", texto_sem_paren).strip()
        base_bruta = limpa_txt(base_bruta)

        # parte secundaria = dentro de [ ]
        secs = re.findall(r"\[(.*?)\]", texto_sem_paren)
        sec_bruta = " ".join(secs).strip()
        sec_bruta = limpa_txt(sec_bruta)

        chaves = re.findall(r"\{(.*?)\}", extra)
        objs = re.findall(r"\((.*?)\)", extra)

        pares = []
        flag_base = " ".join(chaves).replace(" ", "")

        # 1) forma normal preservando ordem original
        if texto_completo:
            for w in extrai_palavras(TXT_maiusc,texto_completo):
                pares.append((w, flag_base, simb))

        # 2) só gera p/s se existir [ ... ]
        if sec_bruta:
            if base_bruta:
                for w in extrai_palavras(TXT_maiusc,base_bruta):
                    pares.append((w, flag_base, "p" + simb))

            for w in extrai_palavras(TXT_maiusc,sec_bruta):
                pares.append((w, flag_base, "s" + simb))

        # 3) partes entre parênteses continuam como antes
        for i, p in enumerate(partes):
            flag = objs[i] if i < len(objs) else ""
            flag = flag.replace(" ", "")
            for w in extrai_palavras(TXT_maiusc,p):
                pares.append((w, flag, simb))

        return pares

    def gera_ABCDDEF(simb,flag):
        A="*"
        for c in simb:
            if c in ["*","#","!","_"]:
                A=c
                break
        B="x"
        if simb.endswith("a") or "gen_fem" in flag:
            B="a"
        elif simb.endswith("o"):
            B="o"
        C="."
        if ":" in simb or "num_plu" in flag or "gen_femnum_plu" in flag:
            C=":"
        D="x"
        if len(simb)>0 and simb[-1] in ["^","v","=","!","?"]:
            D=simb[-1]
        E="x"
        if "1ps" in flag: E="1ps"
        elif "2ps" in flag: E="2ps"
        elif "3ps" in flag: E="3ps"
        elif "1pp" in flag: E="1pp"
        elif "2pp" in flag: E="2pp"
        elif "3pp" in flag: E="3pp"
        F="a" if "abrev" in flag else "x"
        return f"{A},{B},{C},{D},{E},{F}"
    for grupo in DBini:
        if grupo=="⁉️":
            continue
        for linha in DBini[grupo]:
            simb=linha[0]
            txt=linha[1]
            extra=linha[2] if len(linha)>2 else ""
            pares=extrai_pares(simb,txt,extra)
            for palavra,flag,simb_out in pares:
                chave=palavra.strip()
                if not chave:
                    continue
                ABCDEF=gera_ABCDDEF(simb_out,flag)
                novo=f"{simb_out} [{ABCDEF}]"
                if chave not in DB_TXT:
                    DB_TXT[chave]=novo
                else:
                    atual=DB_TXT[chave]
                    if novo not in atual:
                        DB_TXT[chave]=atual+" ; "+novo
    DB_TXT_ordenado=dict(sorted(DB_TXT.items()))
    with open(FILE_NAME_TXT,"w",encoding="utf-8") as f:
        json.dump(DB_TXT_ordenado,f,ensure_ascii=False,indent=2)
    print("DB_TXT estruturado criado e salvo.")
    return DB_TXT_ordenado
    
# ============================================================
# HEURISTICA PORTUGUES TXT => LIU
# ============================================================
def heuristica_pt(TXT_maiusc,palavra, DB_TXT, debug=False, nivel=0):
    # evita loop infinito
    if nivel > 2:
        return None
    p = lower(palavra,TXT_maiusc)
    # -------------------------
    # 0. direto
    # -------------------------
    if p in DB_TXT:
        return DB_TXT[p]
    # =========================
    # FUNÇÕES INTERNAS
    # =========================
    def tenta(base, sufixo=""):
        if base in DB_TXT:
            if debug:
                print(f"NIVEL {nivel}: {p} → {base}")
            return DB_TXT[base] + sufixo
        # tenta recursivo
        return heuristica_pt(TXT_maiusc,base, DB_TXT, debug, nivel+1)
    # =========================
    # 1. plural simples
    # =========================
    if p.endswith("s") and len(p) > 3:
        base = p[:-1]
        r = tenta(base, ":")
        if r: return r
    # =========================
    # 2. feminino o → a
    # =========================
    if p.endswith("a"):
        base = p[:-1] + "o"
        r = tenta(base, "a")
        if r: return r
    # =========================
    # 3. feminino por adição
    # =========================
    if p.endswith("a"):
        base = p[:-1]
        r = tenta(base, "a")
        if r: return r
    # =========================
    # 4. feminino + plural
    # =========================
    if p.endswith("as") and len(p) > 4:
        base = p[:-2]
        r = tenta(base, "a:")
        if r: return r
    # =========================
    # 5. us → uses
    # =========================
    if p.endswith("uses"):
        base = p[:-2]
        r = tenta(base, ":")
        if r: return r
    # =========================
    # 6. plural especial (L)
    # =========================
    if p.endswith("ais"):
        base = p[:-3] + "al"
        r = tenta(base, ":")
        if r: return r
    if p.endswith("eis"):
        base = p[:-3] + "el"
        r = tenta(base, ":")
        if r: return r
    if p.endswith("ois"):
        base = p[:-3] + "ol"
        r = tenta(base, ":")
        if r: return r
    if p.endswith("uis"):
        base = p[:-3] + "ul"
        r = tenta(base, ":")
        if r: return r
    if p.endswith("is") and len(p) > 3:
        base = p[:-2] + "il"
        r = tenta(base, ":")
        if r: return r
    # =========================
    # 7. negação (AGORA RECURSIVA)
    # =========================
    if p.startswith("in") and len(p) > 4:
        base = p[2:]
        r = tenta(base)
        if r:
            return "~" + r
    if p.startswith("im") and len(p) > 4:
        base = p[2:]
        r = tenta(base)
        if r:
            return "~" + r
    if p.startswith("ir") and len(p) > 4:
        base = p[2:]
        r = tenta(base)
        if r:
            return "~" + r
    if p.startswith("des") and len(p) > 5:
        base = p[3:]
        r = tenta(base)
        if r:
            return "~" + r
    # =========================
    # fallback
    # =========================
    return None

# ============================================================
# HEURISTICA INGLES TXT => LIU
# ============================================================
def heuristica_ig(TXT_maiusc,palavra, DB_TXT, debug=False):
    p = lower(palavra,TXT_maiusc)
    # -------------------------
    # 0. tentativa direta
    # -------------------------
    if p in DB_TXT:
        return DB_TXT[p]
    # -------------------------
    # 1. plural simples (s)
    # cars → car
    # -------------------------
    if p.endswith("s") and len(p) > 3:
        base = p[:-1]
        if base in DB_TXT:
            if debug: print("IG plural s:", p, "→", base)
            return DB_TXT[base] + ":"
    # -------------------------
    # 2. plural es
    # boxes → box
    # -------------------------
    if p.endswith("es") and len(p) > 4:
        base = p[:-2]
        if base in DB_TXT:
            if debug: print("IG plural es:", p, "→", base)
            return DB_TXT[base] + ":"
    # -------------------------
    # 3. gerúndio (ing)
    # reading → read
    # -------------------------
    if p.endswith("ing") and len(p) > 5:
        base = p[:-3]
        if base in DB_TXT:
            if debug: print("IG ing:", p, "→", base)
            return DB_TXT[base] + "="
    # -------------------------
    # 4. passado (ed)
    # worked → work
    # -------------------------
    if p.endswith("ed") and len(p) > 4:
        base = p[:-2]
        if base in DB_TXT:
            if debug: print("IG ed:", p, "→", base)
            return DB_TXT[base] + "v"
    # -------------------------
    # 5. negação prefixo
    # unhappy → happy
    # -------------------------
    if p.startswith("un") and len(p) > 4:
        base = p[2:]
        if base in DB_TXT:
            if debug: print("IG neg un:", p, "→", base)
            return "~" + DB_TXT[base]
    if p.startswith("in") and len(p) > 4:
        base = p[2:]
        if base in DB_TXT:
            if debug: print("IG neg in:", p, "→", base)
            return "~" + DB_TXT[base]
    # -------------------------
    # 6. fallback
    # -------------------------
    return None

# ============================================================
# PEGA LIU MAIS ESPECÍFICO E ROTINAS ASSOCIADAS
# ============================================================
def conta_emojis_liu(s):
    return sum(1 for c in s if ord(c) > 10000)

def prioridade_txt_liu(simb):
    simb = re.sub(r"\s*\[.*?\]", "", simb).strip()

    # p... e s... ficam por último
    prioridade_ps = 1 if simb.startswith(("p", "s")) else 0

    n_emojis = conta_emojis_liu(simb)

    # grupo:
    # 0 = melhor: 1 emoji
    # 1 = depois: 0 emoji
    # 2 = depois: >1 emoji
    if n_emojis == 1:
        grupo = 0
    elif n_emojis == 0:
        grupo = 1
    else:
        grupo = 2

    # quanto menos emojis melhor no grupo >1
    return (prioridade_ps, grupo, n_emojis, len(simb))

def pega_melhor_txt_liu(linha_DB):
    partes = [p.strip() for p in linha_DB.split(";") if p.strip()]
    if not partes:
        return ""

    melhor = None
    melhor_chave = None

    for parte in partes:
        m = re.match(r"^(.*?)\s*\[(.*?)\]\s*$", parte)
        if m:
            simb = m.group(1).strip()
        else:
            simb = parte.strip()

        chave = prioridade_txt_liu(simb)

        if melhor is None or chave < melhor_chave:
            melhor = simb
            melhor_chave = chave

    return melhor


def fim_processa_LIU (LIU):
    LIU=LIU.replace("_C"," [[ ")
    LIU=LIU.replace("_J"," ]] ")
    return LIU

def pre_processa_LIU(LIU):
    LIU=LIU.replace("\r\n"," _n ")
    LIU=LIU.replace("\r"," _n ")
    LIU=LIU.replace("\n"," _n ")
    LIU=LIU.replace("[["," _C ",)
    LIU=LIU.replace("]]"," _J ")
    return LIU

def pre_processa_txt(txt):
    txt=txt.replace("\r\n"," _n ")
    txt=txt.replace("\r"," _n ")
    txt=txt.replace("\n"," _n ")
    txt=txt.replace("["," _C ")
    txt=txt.replace("]"," _J ")
    txt=re.sub(r"\.\.\.", " __RETICENCIAS__ ", txt)
    txt=re.sub(r"([\[\]\(\)\{\},;:!?])", r" \1 ", txt)
    txt=re.sub(r"(?<!\.)\.(?!\.)", " . ", txt)
    txt=re.sub(r"\s*__RETICENCIAS__\s*", " ... ", txt)
    txt=re.sub(r" *\n *", "\n", txt)
    return txt

def fim_processa_txt(txt):
    txt=txt.replace("_n","\n")
    txt=txt.replace("_C","[")
    txt=txt.replace("_J","]")
    return txt


# ============================================================
# Converte TXT EM LIU
# ============================================================
def converte_TXT_LIU(TXT_maiusc,linha_TXT, DB_TXT,Ling="pt", debug=False):
    if debug:
        print("\n==============================")
        print("ENTRADA:", linha_TXT)
    linha_TXT=pre_processa_txt(linha_TXT)
    linha = linha_TXT.strip()
    palavras = linha.split()
    palavras_orig = linha.split()
    for i in range(len(palavras)):
       palavras[i]=lower(palavras[i],TXT_maiusc)
       if debug:
          print(f"{palavras[i]} ",end="")
  
    saida = []
    i = 0
    MAX_JANELA = 4

    def limpa_liu(s):
        s = pega_melhor_txt_liu(s)
        s = re.sub(r"\s*\[.*?\]", "", s).strip()
        return s
    while i < len(palavras):
        achou = False
        for tam in range(MAX_JANELA, 0, -1):
            if i + tam > len(palavras):
                continue
            trecho = " ".join(palavras[i:i+tam])
            if debug:
                print(f"TENTANDO: [{trecho}]")
            if trecho in DB_TXT:
                simb = limpa_liu(DB_TXT[trecho])
                if debug:
                    print(f"  ✅ ACHOU: {trecho} → {simb}")
                saida.append(simb)
                i += tam
                achou = True
                break
        if not achou:
            p = palavras[i]
            porig=palavras_orig[i]
            if p in DB_TXT:
                simb = limpa_liu(DB_TXT[p])
                if debug:
                    print(f"  ✔ PALAVRA: {p} → {simb}")
                saida.append(simb)
            else:
                if Ling=="pt":
                   liu = heuristica_pt(TXT_maiusc,p, DB_TXT)
                elif Ling=="ig":
                   liu = heuristica_ig(TXT_maiusc,p, DB_TXT)
                if liu:
                   liu = limpa_liu(liu)
                   saida.append(liu)
                   if debug:
                      print(f"  Achou HEURISTICA{Ling}: {p}")
                else:
                  saida.append(f"'{porig}'")
                  if debug:
                    print(f"  ❌ NAO ACHOU: {p}")
            i += 1
    LIU_OUT = " ".join(saida)
    if debug:
        print("SAIDA:", LIU_OUT)
        print("==============================\n")
    LIU_OUT=fim_processa_LIU(LIU_OUT)    
    return LIU_OUT

# ============================================================
# ACHA RRP LIU
# ============================================================
def localiza_erro_no_liu(TXT_maiusc,linha_LIU, txt_original, txt_volta, DBLIU, ALIAS_BD):
    def limpa_tokens(txt):
        txt = txt.replace(",", " , ").replace(".", " . ").replace("?", " ? ").replace("!", " ! ").replace(";", " ; ").replace(":", " : ")
        return txt.strip().split()

    tokens_liu = linha_LIU.split()
    orig_tokens = limpa_tokens(txt_original)
    volta_tokens = limpa_tokens(txt_volta)

    # gera texto de cada símbolo LIU isolado
    saida_tokens = []
    for simb in tokens_liu:
        txt_parcial = converte_LIU_TXT(
            TXT_maiusc,
            simb,
            DBLIU,
            ALIAS_BD,
            usa_PAD=True,
            usa_EXT=True,
            usa_EXPLIC=False,
            Usa_Key=True,
            debug=False,
            debugw=False
        )
        saida_tokens.append((simb, txt_parcial))

    erros = []
    tam = max(len(orig_tokens), len(volta_tokens))

    for i in range(tam):
        esperado = orig_tokens[i] if i < len(orig_tokens) else ""
        obtido = volta_tokens[i] if i < len(volta_tokens) else ""

        if esperado != obtido:
            simb_msg = ""

            # tenta casar com o símbolo na mesma posição
            if i < len(saida_tokens):
                simb_ruim, txt_gerado = saida_tokens[i]
                simb_msg = f"{simb_ruim} => {txt_gerado}"
            else:
                simb_msg = "símbolo não localizado"

            erros.append(f"{simb_msg} : esperado '{esperado}' mas gerou '{obtido}'")

    if not erros:
        return "converte OK"

    return "TXT->LIU: pode ter erro em: " + " ; ".join(erros)

# ============================================================
# Converte TXT EM LIU E TESTA
# ============================================================
def converte_TXT_LIU_TST(TXT_maiusc,txt, DB_TXT, DBLIU, ALIAS_BD, Ling='pt', debug=False):
    LIU_OUT = converte_TXT_LIU(TXT_maiusc,txt, DB_TXT, Ling=Ling, debug=debug)
    LIU_POS = pos_processa(LIU_OUT, ALIAS_BD)
    TXT_VOLTA = converte_LIU_TXT(TXT_maiusc,LIU_POS, DBLIU, ALIAS_BD, debug=False, debugw=False)

    if txt == TXT_VOLTA:
        msg = "converte OK"
    else:
        msg = localiza_erro_no_liu(TXT_maiusc,LIU_POS, txt, TXT_VOLTA, DBLIU, ALIAS_BD)

    return msg, LIU_OUT

# ============================================================
# Converte LIU EM TXT E TESTA
# ============================================================
def converte_LIU_TXT_TST(TXT_maiusc,linha_LIU, DBLIU, DB_TXT, ALIAS_BD, Ling="pt", debug=False):
    def limpa_tokens(txt):
        txt = txt.replace(",", " , ").replace(".", " . ").replace("?", " ? ").replace("!", " ! ").replace(";", " ; ").replace(":", " : ")
        return txt.strip().split()

    # 1) LIU original pos-processado
    linha_LIU=pre_processa_LIU(linha_LIU)
    LINHA_REF = pos_processa(linha_LIU, ALIAS_BD)

    # 2) primeira volta LIU -> TXT
    TXT1 = converte_LIU_TXT(TXT_maiusc,LINHA_REF, DBLIU, ALIAS_BD, debug=debug, debugw=False)
    
    # 3) TXT1 -> LIU
    LIU2 = converte_TXT_LIU(TXT_maiusc,TXT1, DB_TXT, Ling=Ling, debug=False)
    LIU2 = pos_processa(LIU2, ALIAS_BD)

    # 4) LIU2 -> TXT2
    TXT2 = converte_LIU_TXT(TXT_maiusc,LIU2, DBLIU, ALIAS_BD, debug=False, debugw=False)
   # print(f"LUI->TXT: TXT1={TXT1}, TXT2={TXT2}")
    # 5) se TXT1 == TXT2, então está estável
    if TXT1 == TXT2:
        msg = "converte OK"
        return msg, TXT1

    # 6) localizar onde TXT mudou
    tokens_liu = LINHA_REF.split()
    txt1_tokens = limpa_tokens(TXT1)
    txt2_tokens = limpa_tokens(TXT2)

    # texto gerado por cada símbolo LIU isolado
    saida_tokens = []
    for simb in tokens_liu:
        txt_parcial = converte_LIU_TXT(
            TXT_maiusc,
            simb,
            DBLIU,
            ALIAS_BD,
            usa_PAD=True,
            usa_EXT=True,
            usa_EXPLIC=False,
            Usa_Key=True,
            debug=False,
            debugw=False
        )
        saida_tokens.append((simb, txt_parcial))

    erros = []
    tam = max(len(txt1_tokens), len(txt2_tokens))

    for i in range(tam):
        esperado = txt1_tokens[i] if i < len(txt1_tokens) else ""
        obtido = txt2_tokens[i] if i < len(txt2_tokens) else ""

        if esperado != obtido:
            if i < len(saida_tokens):
                simb_ruim, txt_gerado = saida_tokens[i]
                item = f"{simb_ruim} => {txt_gerado} : esperado '{esperado}' mas gerou '{obtido}'"
            else:
                item = f"posição {i} : esperado '{esperado}' mas gerou '{obtido}'"

            if item not in erros:
                erros.append(item)

    if not erros:
        msg = f"LIU->TXT: pode ter erro | TXT1='{TXT1}' | TXT2='{TXT2}'"
    else:
        msg = "LIU->TXT: pode ter erro em: " + " ; ".join(erros)
    TXT1=fim_processa_txt(TXT1)
    return msg,TXT1 



