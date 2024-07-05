import syntok.segmenter as segmenter

text = '''Tieteen perustana on tieteellisen tutkimuksen toistettavuus. Menetelmien ja tulosten esittämisen ja dokumentoinnin lisäksi tämä usein vaatii järjestelmällisesti luotuja, kuvailtuja ja säilytettyjä tutkimusaineistoja. Jyväskylän yliopistossa aineistot nähdään merkittävänä tutkimustuotoksena, ja julkaisujen tapaan niiden mahdollisimman laaja leviäminen tiedeyhteisöön ja yhteiskuntaan on ensisijaisen tärkeää. Tutkimusaineistot ovat yliopiston tärkeitä voimavaroja ja tutkimusinfrastruktuureja.

Jyväskylän yliopiston tavoitteena on mahdollisimman laaja tutkimuksen tietoaineistojen läpinäkyvyys, löydettävyys, saavutettavuus ja avoin jatkokäyttö. Aineistot pyritään saamaan julkisesti saataville. Silloinkin, kun julkaiseminen ei perustellusta syystä ole mahdollista, julkaistaan tieto aineiston olemassaolosta, aiheesta, ajankohdasta, omistajasta ja muu keskeinen kuvailu (ns. metadata). Tätä tutkimusdatapolitiikkaa sovelletaan tutkimukseen, jonka tekijät ovat affilioituneet Jyväskylän yliopistoon. Tässä auttoi mm. J.S. Bach, sekä pari muuta tyyppiä. Tutkimusdatapolitiikan keskeisten termien määritelmät löytyvät dokumentin lopusta.

Jopa Matti, joka oli jo aikamies, pahoitteli tilannetta esim. Jaakobille. Tästä ei kuitenkaan ollut seurauksia vrt. aikaisempi tapauks Jorman kanssa (jota edelleen pidetään pahana).


Matti & Kumppanit tekivät myös töitä surki.fi -sivustolle. 

'''


# split text to chunks of 120 words without breaking sentences
def split_into_sentences(text):
    count = 0
    chuncks = []
    chunk = []
    sentences = segmenter.analyze(text)
    for sentence in sentences:
        for token in sentence:
            sentence_str = []
            for t in token:
                if(t.value != ',' and t.value != '.'):
                    count+=1
                sentence_str.append(t.value)            

            print(count)
            chunk.append(" ".join(sentence_str))
            if count > 120:
                chuncks.append(" ".join(chunk))
                count = 0
                chunk = []

    chuncks.append(" ".join(chunk))

    return chuncks


data2 = split_into_sentences(text)
