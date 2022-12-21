import sys


def f(text0):
    s = 'cp037 cp1006 cp1250 cp1251 cp1253 cp1254 cp1255 cp1256 cp1257 cp1258 cp437 cp720 cp737 cp775 cp850 cp852 ' \
        'cp855 ' \
        'cp864 cp866 cp869 cp874 cp875 hp_roman8 iso8859_10 iso8859_16 iso8859_4 iso8859_5 koi8_r latin_1' \
        'mac_croatian mac_greek mac_iceland mac_latin2'

    s = s.split()
    for i in s:
        try:
            text1 = text0.encode(i)
            text1 = text1.decode(i)
        except Exception:
            continue
        try:
            # text4 = text1.decode('UTF-8')
            text4 = text1
            if 'ПРОЦ' in text4 and 'КНЦ' in text4 and 'ВЫВОД' in text4:
                return text4
        except UnicodeDecodeError:
            pass

        for j in s:
            try:
                text2 = text1.encode(j)
                text2 = text1.decode(j)
            except Exception:
                continue

            for k in s:
                try:
                    text3 = text2.encode(k)
                except Exception:
                    continue
                try:
                    text4 = text3.decode('UTF-8')
                    if 'ПРОЦ' in text4 and 'КНЦ' in text4 and 'ВЫВОД' in text4:
                        return text4
                except UnicodeDecodeError:
                    continue


def f0(text):
    s = 'cp037 cp1006 cp1250 cp1251 cp1253 cp1254 cp1255 cp1256 cp1257 cp1258 cp437 cp720 cp737 cp775 cp850 cp852 ' \
        'cp855 ' \
        'cp864 cp866 cp869 cp874 cp875 hp_roman8 iso8859_10 iso8859_16 iso8859_4 iso8859_5 koi8_r latin_1' \
        'mac_croatian mac_greek mac_iceland mac_latin2'

    s = s.split()
    # for i in s:
    #     for j in s:
    #         for
    return text.decode('UTF-8', errors='replace').encode('latin1', errors='replace').decode('CP1251', errors='replace')


text0 = sys.stdin.buffer.read().decode('koi8-r')#
print(text0)

print(f(text0))
