import json, os, sys
from collections import Counter

base = os.path.dirname(os.path.abspath(__file__))
ver  = "RV1909-es"
p    = os.path.join(base, "data", "versions", ver + ".json")
print("FILE:", p)

with open(p, "r", encoding="utf-8-sig") as f:
    data = json.load(f)

def t(x):
    return type(x).__name__

print("TOP_TYPE:", t(data))
if isinstance(data, dict):
    keys = list(data.keys())
    print("TOP_KEYS_COUNT:", len(keys))
    print("TOP_KEYS_SAMPLE:", keys[:40])

    # medir tipos de valores
    type_counts = Counter(t(v) for v in data.values())
    print("TOP_VALUE_TYPES:", dict(type_counts))

    # elegir candidato: clave que parezca contener libros/chapters/verses
    candidates = []
    for k in keys:
        lk = k.lower()
        if any(s in lk for s in ["books","book","biblia","bible","data","verses","verse","chapters","chapter","texto","text","version"]):
            candidates.append(k)
    print("CANDIDATE_KEYS:", candidates[:30])

    # intentar bajar 3 niveles en cada candidato y mostrar ejemplo
    def preview(obj, label):
        print("\n== PREVIEW:", label, "TYPE:", t(obj))
        if isinstance(obj, dict):
            kk = list(obj.keys())
            print("keys:", kk[:30])
            if kk:
                v = obj[kk[0]]
                print("first_key:", kk[0], "first_type:", t(v))
                if isinstance(v, (dict, list)):
                    preview(v, label + " -> " + str(kk[0]))
                else:
                    s = str(v)
                    print("first_value_sample:", s[:200])
        elif isinstance(obj, list):
            print("len:", len(obj))
            if obj:
                v = obj[0]
                print("first_type:", t(v))
                if isinstance(v, (dict, list)):
                    preview(v, label + " -> [0]")
                else:
                    s = str(v)
                    print("first_value_sample:", s[:200])

    for k in candidates[:10]:
        preview(data.get(k), k)

    # si no hay candidatos, igual mostrar un preview genérico del primer valor
    if not candidates and keys:
        k0 = keys[0]
        preview(data.get(k0), "FIRST_KEY=" + k0)

else:
    # si es lista, mostrar primer elemento
    if isinstance(data, list) and data:
        v = data[0]
        print("LIST_LEN:", len(data))
        print("FIRST_TYPE:", t(v))
        if isinstance(v, dict):
            kk = list(v.keys())
            print("FIRST_KEYS:", kk[:40])
        else:
            print("FIRST_VALUE_SAMPLE:", str(v)[:200])
