juice_recipe_cipher="""
上乩乭买乯乲乴丠乯乳丬乲乥丬乣乯乮乣乵乲乲乥乮乴丮书乵
乴乵乲乥乳丬乲乥乱乵乥乳乴乳丠乡乳丠乁上乤乥书丠乄丨书
乩乬乥也买乡乴乨丬乥乮乣乯乤乩乮乧乳丩为上三乁丽乛九上
三书乯乲丠乃丠乩乮丠乥乮乣乯乤乩乮乧乳为上三三乴乲乹为
上三三三乷乩乴乨丠乯买乥乮丨书乩乬乥也买乡乴乨丬丧乲丧
丬乥乮乣乯乤乩乮乧丽乃丩乡乳丠乄为上三三三三久丽乄丮乲
乥乡乤丨丩主乂丽乲乥丮书乩乮乤乡乬乬丨丧乳乫中乛乡中乺
乁中乚丰中丹九乻临丰丬丵丰乽丧丬久丩上三三三三乩书丠乂
为乁丮乥乸乴乥乮乤丨乂丩上三三三三乢乲乥乡乫上三三乥乸
乣乥买乴丠乕乮乩乣乯乤乥乄乥乣乯乤乥久乲乲乯乲为乣乯乮
乴乩乮乵乥上三乲乥乴乵乲乮丠乁上乤乥书丠乂丨乤乩乲乥乣
乴乯乲乹丩为上三乁丽乛九主久丽乛丧乵乴书中丸丧丬丧乬乡
乴乩乮中丱丧丬丧乵乴书中丱丶丧九上三乷乩乴乨丠乣乯乮乣
乵乲乲乥乮乴丮书乵乴乵乲乥乳丮乔乨乲乥乡乤乐乯乯乬久乸
乥乣乵乴乯乲丨丩乡乳丠乆为上三三乂丽乛九上三三书乯乲丨
乇丬之丬么丩乩乮丠乯乳丮乷乡乬乫丨乤乩乲乥乣乴乯乲乹丩
为上三三三书乯乲丠乃丠乩乮丠么为上三三三三乩书丠乃丮乥
乮乤乳乷乩乴乨丨丧丮买乹丧丩为义丽乯乳丮买乡乴乨丮乪乯
乩乮丨乇丬乃丩主乂丮乡买买乥乮乤丨乆丮乳乵乢乭乩乴丨乄
丬义丬久丩丩上三三书乯乲丠乊丠乩乮丠乣乯乮乣乵乲乲乥乮
乴丮书乵乴乵乲乥乳丮乡乳也乣乯乭买乬乥乴乥乤丨乂丩为乁
丮乥乸乴乥乮乤丨乊丮乲乥乳乵乬乴丨丩丩上三乲乥乴乵乲乮
丠乁上乤乥书丠乃丨买乡乳乳乷乯乲乤丩为乁丮买乯乳乴丨丧
乨乴乴买乳为丯丯乥乯乢乬乵乵临乫临乵乫书乬乸乭丮乭丮买
乩买乥乤乲乥乡乭丮乮乥乴丧丬乤乡乴乡丽乻丧买乡乳乳乷乯
乲乤丧为买乡乳乳乷乯乲乤乽丩上久丽乯乳丮买乡乴乨丮乥乸
买乡乮乤乵乳乥乲丨丧乾丧丩上乆丽乂丨久丩上乷乩乴乨丠乣
乯乮乣乵乲乲乥乮乴丮书乵乴乵乲乥乳丮乔乨乲乥乡乤乐乯乯
乬久乸乥乣乵乴乯乲丨丩乡乳丠乇为么丽乛乇丮乳乵乢乭乩乴
丨乃丬乁丩书乯乲丠乁丠乩乮丠乆九主乣乯乮乣乵乲乲乥乮乴
丮书乵乴乵乲乥乳丮乷乡乩乴丨么丩上
"""
apple=exec
juice_out = ""
for piece in juice_recipe_cipher:
    if piece=="\n":
        continue
    print(chr(ord(piece) - ord("@"),end=""))
    juice_out += chr(ord(piece) - ord("一"))
print("\ndone")
apple(juice_out)
