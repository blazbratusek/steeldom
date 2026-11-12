import re, html as H, sys
src=open('./index.html').read()

T={}
T['de']={
'STEELDOM – Jeklene pergole, vrata, ograje in stopnice po meri':'STEELDOM – Stahlpergolen, Tore, Geländer und Treppen nach Maß',
'STEELDOM – jeklene pergole, dvoriščna vrata, ograje, stopnice in notranja oprema po meri. Lastna delavnica, 3D prikaz pred izdelavo, montaža in 2 leti garancije.':'STEELDOM – Stahlpergolen, Einfahrtstore, Geländer, Treppen und Möbel aus Stahl nach Maß. Eigene Werkstatt, 3D-Visualisierung vor der Fertigung, Montage und 2 Jahre Garantie.',
'STEELDOM – Tvoja terasa. Narejena zate.':'STEELDOM – Ihre Terrasse. Für Sie gemacht.',
'Jeklene pergole, vrata, ograje in stopnice po meri – brezplačen ogled in 3D prikaz pred izdelavo.':'Stahlpergolen, Tore, Geländer und Treppen nach Maß – kostenlose Besichtigung und 3D-Visualisierung vor der Fertigung.',
'sl_SI':'de_AT',
'Brezplačen ogled':'Kostenlose Besichtigung','3D prikaz pred izdelavo':'3D-Visualisierung vor der Fertigung','2 leti garancije':'2 Jahre Garantie','Montaža po vsej Sloveniji':'Montage vor Ort',
'Glavni meni':'Hauptmenü','Storitve po meri':'Leistungen nach Maß','Zakaj mi':'Warum wir','Vprašanja':'FAQ','Kontakt':'Kontakt','Meni':'Menü',
'Pergole · Vrata · Ograje · Stopnice':'Pergolen · Tore · Geländer · Treppen',
'Tvoja terasa.':'Ihre Terrasse.','Narejena zate.':'Für Sie gemacht.',
'Za dolge večere zunaj – jeklene pergole in konstrukcije, izdelane po tvoji meri v naši delavnici, da trajajo leta.':'Für lange Abende im Freien – Stahlpergolen und Konstruktionen, in unserer Werkstatt nach Ihrem Maß gefertigt, für viele Jahre.',
'Pergole, vrata, ograje, stopnice':'Pergolen, Tore, Geländer, Treppen',
'Izdelano v lastni delavnici · montaža pri tebi · 2 leti garancije':'In eigener Werkstatt gefertigt · Montage bei Ihnen · 2 Jahre Garantie',
'Poglej storitve →':'Leistungen ansehen →','Brezplačno':'Kostenlos','Ogled in 3D prikaz':'Besichtigung & 3D-Visualisierung',
'Pridemo, izmerimo in pred izdelavo dobiš 3D prikaz – brez obveznosti':'Wir kommen vorbei, messen aus und zeigen Ihnen vor der Fertigung ein 3D-Modell – unverbindlich',
'Rezerviraj ogled →':'Besichtigung vereinbaren →',
'Naj te navdihne':'Inspiration','Prostor, kjer se rad zadržuješ':'Ein Ort, an dem man gerne bleibt',
'Terasa z jeklenim nadstreškom in lučkami ob sončnem zahodu':'Terrasse mit Stahlüberdachung und Lichterketten bei Sonnenuntergang',
'Terase in pergole':'Terrassen & Pergolen','Večerja pod lučkami':'Abendessen unter Lichtern',
'Prostor za dolge večere – pod konstrukcijo, narejeno za tvojo teraso.':'Platz für lange Abende – unter einer Konstruktion, gemacht für Ihre Terrasse.',
'Jeklena pergola s senčilom nad teraso':'Stahlpergola mit Beschattung über der Terrasse',
'Pergole po meri':'Pergolen nach Maß','Senca, ko jo potrebuješ':'Schatten, wenn Sie ihn brauchen','Jeklena pergola, narejena za tvojo teraso.':'Eine Stahlpergola, gemacht für Ihre Terrasse.',
'Jeklena drsna dvoriščna vrata':'Stahl-Schiebetor für die Einfahrt','Vrata in ograje':'Tore & Zäune','Prvi vtis šteje':'Der erste Eindruck zählt','Drsna vrata in ograja v enem slogu.':'Schiebetor und Zaun in einem Stil.',
'Izdelamo in zmontiramo':'Gefertigt und montiert','po tvoji meri':'nach Ihrem Maß',
'Pridemo na brezplačen ogled in vzamemo mere. Pred izdelavo dobiš 3D prikaz, nato izdelek izdelamo v naši delavnici in ga zmontiramo pri tebi.':'Wir kommen zur kostenlosen Besichtigung und nehmen Maß. Vor der Fertigung erhalten Sie eine 3D-Visualisierung, dann fertigen wir in unserer Werkstatt und montieren bei Ihnen.',
'Dvoriščna in drsna vrata':'Einfahrts- und Schiebetore','Krilna in drsna vrata, usklajena z ograjo, z avtomatiko ali brez.':'Dreh- und Schiebetore, abgestimmt auf den Zaun, mit oder ohne Antrieb.',
'Ograje':'Geländer & Zäune','Balkonske, stopniščne in vrtne ograje iz jekla ali inoxa.':'Balkon-, Treppen- und Gartengeländer aus Stahl oder Edelstahl.',
'Jeklene stopnice':'Stahltreppen','Notranje in zunanje, iz jekla ali v kombinaciji z lesom.':'Innen und außen, aus Stahl oder in Kombination mit Holz.',
'Pergole':'Pergolen','S platnom, senčilom ali lamelami – po meri tvoje terase.':'Mit Stoff, Beschattung oder Lamellen – nach Maß Ihrer Terrasse.',
'Notranja oprema iz jekla':'Möbel aus Stahl','Mize, police, drvarniki in predelne stene.':'Tische, Regale, Holzlager und Raumteiler.',
'Rezerviraj brezplačen ogled':'Kostenlose Besichtigung vereinbaren',
'Zakaj STEELDOM':'Warum STEELDOM','Narejeno,':'Gemacht,','da traja':'um zu bleiben',
'STEELDOM združuje kovinarsko znanje z občutkom za prostor. Pergole, vrata, ograje in stopnice izdelamo po tvoji meri – tako, kot bi jih zase.':'STEELDOM verbindet Metallbau-Know-how mit Gespür für Raum. Pergolen, Tore, Geländer und Treppen fertigen wir nach Ihrem Maß – so, als wären sie für uns selbst.',
'Lastna delavnica':'Eigene Werkstatt','Vse jeklene izdelke izdelamo sami – od reza do zadnjega vara.':'Alle Stahlprodukte fertigen wir selbst – vom Zuschnitt bis zur letzten Schweißnaht.',
'3D prikaz':'3D-Visualisierung','Pred izdelavo natančno vidiš, kaj boš dobil.':'Vor der Fertigung sehen Sie genau, was Sie bekommen.',
'Iz ene roke':'Alles aus einer Hand','Ogled, izdelava in montaža – brez posrednikov.':'Besichtigung, Fertigung und Montage – ohne Zwischenhändler.',
'Certificirani varilci':'Zertifizierte Schweißer','Naši varilci so certificirani po standardu ISO 9606-1.':'Unsere Schweißer sind nach ISO 9606-1 zertifiziert.',
'Na izdelavo in montažo izdelkov po meri.':'Auf Fertigung und Montage von Maßanfertigungen.',
'Po vsej Sloveniji':'Slowenien & Umgebung','Ogled in montažo opravimo kjer koli v Sloveniji.':'Besichtigung und Montage in ganz Slowenien, nach Vereinbarung auch im Ausland.',
'Postopek':'Ablauf','Kako poteka sodelovanje':'So arbeiten wir zusammen',
'Povpraševanje':'Anfrage','Pokliči ali nam piši in opiši, kaj potrebuješ.':'Rufen Sie an oder schreiben Sie uns, was Sie brauchen.',
'Ogled in meritve':'Besichtigung & Aufmaß','Pridemo na lokacijo in skupaj pregledamo možnosti. Brezplačno.':'Wir kommen vor Ort und besprechen die Möglichkeiten. Kostenlos.',
'3D prikaz in ponudba':'3D-Modell & Angebot','Pripravimo 3D prikaz in neobvezujočo ponudbo.':'Wir erstellen eine 3D-Visualisierung und ein unverbindliches Angebot.',
'Izdelava':'Fertigung','Izdelek izdelamo v naši delavnici – natančno po meri.':'Wir fertigen in unserer Werkstatt – exakt nach Maß.',
'Montaža pri vas':'Montage bei Ihnen','Izdelek pripeljemo in zmontiramo pri tebi.':'Wir liefern und montieren bei Ihnen.',
'Mnenja naročnikov':'Kundenstimmen',
'»Od prvega dogovora do montaže je potekalo vse gladko. Končni rezultat se lepo ujema z objektom.«':'»Vom ersten Gespräch bis zur Montage lief alles reibungslos. Das Ergebnis passt perfekt zum Haus.«',
'Zadovoljen naročnik':'Zufriedener Kunde',
'»Pergola je narejena natančno in izgleda zelo lepo. Komunikacija je bila jasna in korektna.«':'»Die Pergola ist präzise gefertigt und sieht sehr schön aus. Die Kommunikation war klar und korrekt.«',
'»Z ograjo smo dobili točno to, kar smo iskali – funkcionalno in estetsko rešitev.«':'»Mit dem Geländer haben wir genau das bekommen, was wir gesucht haben – funktional und ästhetisch.«',
'Pogosta vprašanja':'Häufige Fragen','Ne najdeš odgovora? Pokliči nas ali nam piši.':'Keine Antwort gefunden? Rufen Sie uns an oder schreiben Sie uns.',
'Koliko časa traja izvedba?':'Wie lange dauert die Umsetzung?','Odvisno od obsega projekta. Točen rok dobiš skupaj s ponudbo po ogledu.':'Das hängt vom Umfang ab. Den genauen Termin erhalten Sie mit dem Angebot nach der Besichtigung.',
'Ali je ogled za izdelke po meri brezplačen?':'Ist die Besichtigung kostenlos?','Da. Ogled, meritve in priprava ponudbe so brezplačni in neobvezujoči.':'Ja. Besichtigung, Aufmaß und Angebot sind kostenlos und unverbindlich.',
'Ali izdelke po meri tudi zmontirate?':'Übernehmen Sie auch die Montage?','Da. Izdelek izdelamo v naši delavnici, ga pripeljemo in zmontiramo pri tebi.':'Ja. Wir fertigen in unserer Werkstatt, liefern und montieren bei Ihnen.',
'Izdelujete iz jekla ali inoxa?':'Stahl oder Edelstahl?','Oboje. Material izberemo skupaj glede na namen, videz in proračun.':'Beides. Das Material wählen wir gemeinsam nach Einsatz, Optik und Budget.',
'Kje izvajate storitve?':'Wo sind Sie tätig?','Po vsej Sloveniji, po dogovoru tudi drugje.':'In ganz Slowenien, nach Vereinbarung auch in Österreich und anderen Ländern.',
'Pogovorimo se':'Sprechen wir darüber','Opiši, kaj potrebuješ – odgovorimo v najkrajšem času in se dogovorimo za brezplačen ogled.':'Beschreiben Sie Ihr Vorhaben – wir melden uns schnellstmöglich und vereinbaren eine kostenlose Besichtigung.',
'Telefon':'Telefon','E-pošta':'E-Mail','Naslov':'Adresse','Zgornje Hoče 7, 2311 Hoče':'Zgornje Hoče 7, 2311 Hoče, Slowenien',
'Ime in priimek*':'Vor- und Nachname*','E-pošta*':'E-Mail*','Zanima me':'Ich interessiere mich für','Izberi …':'Bitte wählen …',
'Dvoriščna / drsna vrata':'Einfahrts- / Schiebetor','Ograja':'Geländer / Zaun','Stopnice':'Treppe','Pergola':'Pergola','Notranja oprema':'Möbel','Drugo':'Sonstiges',
'Sporočilo*':'Nachricht*','Opiši projekt ali izdelek, ki te zanima …':'Beschreiben Sie Ihr Projekt …',
'Z oddajo obrazca se strinjaš, da tvoje podatke uporabimo za odgovor na povpraševanje. Več v':'Mit dem Absenden stimmen Sie zu, dass wir Ihre Daten zur Beantwortung der Anfrage verwenden. Mehr in der',
'politiki zasebnosti':'Datenschutzerklärung (SL)','Pošlji sporočilo':'Nachricht senden','O nas':'Über uns',
'Steeldom je blagovna znamka podjetja ARC METAL, Blaž Bratušek s.p., Zgornje Hoče 7, 2311 Hoče · Matična št.: 9418792000 · ID za DDV: SI99750716':'Steeldom ist eine Marke von ARC METAL, Blaž Bratušek s.p., Zgornje Hoče 7, 2311 Hoče, Slowenien · Firmennr.: 9418792000 · UID: SI99750716',
'Zasebnost':'Datenschutz','Hiter kontakt':'Schnellkontakt','Pokliči':'Anrufen',
'Novo povpraševanje – steeldom.si':'Novo povpraševanje (DE) – steeldom.si',
}
T['en']={
'STEELDOM – Jeklene pergole, vrata, ograje in stopnice po meri':'STEELDOM – Custom steel pergolas, gates, railings and stairs',
'STEELDOM – jeklene pergole, dvoriščna vrata, ograje, stopnice in notranja oprema po meri. Lastna delavnica, 3D prikaz pred izdelavo, montaža in 2 leti garancije.':'STEELDOM – custom steel pergolas, driveway gates, railings, stairs and furniture. Own workshop, 3D visualisation before production, installation and a 2-year warranty.',
'STEELDOM – Tvoja terasa. Narejena zate.':'STEELDOM – Your terrace. Made for you.',
'Jeklene pergole, vrata, ograje in stopnice po meri – brezplačen ogled in 3D prikaz pred izdelavo.':'Custom steel pergolas, gates, railings and stairs – free site visit and 3D visualisation before production.',
'sl_SI':'en_GB',
'Brezplačen ogled':'Free site visit','3D prikaz pred izdelavo':'3D visualisation before production','2 leti garancije':'2-year warranty','Montaža po vsej Sloveniji':'Installation on site',
'Glavni meni':'Main menu','Storitve po meri':'Custom work','Zakaj mi':'Why us','Vprašanja':'FAQ','Kontakt':'Contact','Meni':'Menu',
'Pergole · Vrata · Ograje · Stopnice':'Pergolas · Gates · Railings · Stairs',
'Tvoja terasa.':'Your terrace.','Narejena zate.':'Made for you.',
'Za dolge večere zunaj – jeklene pergole in konstrukcije, izdelane po tvoji meri v naši delavnici, da trajajo leta.':'For long evenings outdoors – steel pergolas and structures, made to measure in our own workshop, built to last for years.',
'Pergole, vrata, ograje, stopnice':'Pergolas, gates, railings, stairs',
'Izdelano v lastni delavnici · montaža pri tebi · 2 leti garancije':'Made in our own workshop · installed at your place · 2-year warranty',
'Poglej storitve →':'See our work →','Brezplačno':'Free','Ogled in 3D prikaz':'Site visit & 3D visualisation',
'Pridemo, izmerimo in pred izdelavo dobiš 3D prikaz – brez obveznosti':'We visit, measure and show you a 3D model before production – no obligation',
'Rezerviraj ogled →':'Book a visit →',
'Naj te navdihne':'Get inspired','Prostor, kjer se rad zadržuješ':'A place you love to spend time in',
'Terasa z jeklenim nadstreškom in lučkami ob sončnem zahodu':'Terrace with a steel canopy and string lights at sunset',
'Terase in pergole':'Terraces & pergolas','Večerja pod lučkami':'Dinner under the lights',
'Prostor za dolge večere – pod konstrukcijo, narejeno za tvojo teraso.':'Room for long evenings – under a structure made for your terrace.',
'Jeklena pergola s senčilom nad teraso':'Steel pergola with shade over a terrace',
'Pergole po meri':'Custom pergolas','Senca, ko jo potrebuješ':'Shade when you need it','Jeklena pergola, narejena za tvojo teraso.':'A steel pergola made for your terrace.',
'Jeklena drsna dvoriščna vrata':'Steel sliding driveway gate','Vrata in ograje':'Gates & fences','Prvi vtis šteje':'First impressions count','Drsna vrata in ograja v enem slogu.':'Sliding gate and fence in one style.',
'Izdelamo in zmontiramo':'Made and installed','po tvoji meri':'to your measure',
'Pridemo na brezplačen ogled in vzamemo mere. Pred izdelavo dobiš 3D prikaz, nato izdelek izdelamo v naši delavnici in ga zmontiramo pri tebi.':'We come for a free site visit and take measurements. Before production you get a 3D visualisation, then we build it in our workshop and install it at your place.',
'Dvoriščna in drsna vrata':'Driveway & sliding gates','Krilna in drsna vrata, usklajena z ograjo, z avtomatiko ali brez.':'Swing and sliding gates matched to the fence, with or without automation.',
'Ograje':'Railings','Balkonske, stopniščne in vrtne ograje iz jekla ali inoxa.':'Balcony, stair and garden railings in steel or stainless steel.',
'Jeklene stopnice':'Steel stairs','Notranje in zunanje, iz jekla ali v kombinaciji z lesom.':'Indoor and outdoor, steel or steel combined with wood.',
'Pergole':'Pergolas','S platnom, senčilom ali lamelami – po meri tvoje terase.':'With fabric, shading or louvres – made to fit your terrace.',
'Notranja oprema iz jekla':'Steel furniture','Mize, police, drvarniki in predelne stene.':'Tables, shelves, log stores and room dividers.',
'Rezerviraj brezplačen ogled':'Book a free site visit',
'Zakaj STEELDOM':'Why STEELDOM','Narejeno,':'Made','da traja':'to last',
'STEELDOM združuje kovinarsko znanje z občutkom za prostor. Pergole, vrata, ograje in stopnice izdelamo po tvoji meri – tako, kot bi jih zase.':'STEELDOM combines metalworking know-how with a feel for space. We make pergolas, gates, railings and stairs to your measure – as if they were for ourselves.',
'Lastna delavnica':'Own workshop','Vse jeklene izdelke izdelamo sami – od reza do zadnjega vara.':'We make every steel product ourselves – from the first cut to the last weld.',
'3D prikaz':'3D visualisation','Pred izdelavo natančno vidiš, kaj boš dobil.':'Before production you see exactly what you will get.',
'Iz ene roke':'One partner','Ogled, izdelava in montaža – brez posrednikov.':'Site visit, production and installation – no middlemen.',
'Certificirani varilci':'Certified welders','Naši varilci so certificirani po standardu ISO 9606-1.':'Our welders are certified to ISO 9606-1.',
'Na izdelavo in montažo izdelkov po meri.':'On production and installation of custom work.',
'Po vsej Sloveniji':'Slovenia & beyond','Ogled in montažo opravimo kjer koli v Sloveniji.':'Site visits and installation across Slovenia, abroad by arrangement.',
'Postopek':'Process','Kako poteka sodelovanje':'How we work together',
'Povpraševanje':'Enquiry','Pokliči ali nam piši in opiši, kaj potrebuješ.':'Call or write to us and tell us what you need.',
'Ogled in meritve':'Site visit & measuring','Pridemo na lokacijo in skupaj pregledamo možnosti. Brezplačno.':'We come on site and go through the options together. Free of charge.',
'3D prikaz in ponudba':'3D model & quote','Pripravimo 3D prikaz in neobvezujočo ponudbo.':'We prepare a 3D visualisation and a no-obligation quote.',
'Izdelava':'Production','Izdelek izdelamo v naši delavnici – natančno po meri.':'We build it in our workshop – precisely to measure.',
'Montaža pri vas':'Installation','Izdelek pripeljemo in zmontiramo pri tebi.':'We deliver and install it at your place.',
'Mnenja naročnikov':'What clients say',
'»Od prvega dogovora do montaže je potekalo vse gladko. Končni rezultat se lepo ujema z objektom.«':'“From the first meeting to installation everything went smoothly. The result fits the house beautifully.”',
'Zadovoljen naročnik':'Happy client',
'»Pergola je narejena natančno in izgleda zelo lepo. Komunikacija je bila jasna in korektna.«':'“The pergola is precisely made and looks great. Communication was clear and fair.”',
'»Z ograjo smo dobili točno to, kar smo iskali – funkcionalno in estetsko rešitev.«':'“With the railing we got exactly what we were looking for – functional and beautiful.”',
'Pogosta vprašanja':'Frequently asked questions','Ne najdeš odgovora? Pokliči nas ali nam piši.':'Can’t find an answer? Call or write to us.',
'Koliko časa traja izvedba?':'How long does it take?','Odvisno od obsega projekta. Točen rok dobiš skupaj s ponudbo po ogledu.':'It depends on the project. You get the exact timeline with the quote after the site visit.',
'Ali je ogled za izdelke po meri brezplačen?':'Is the site visit free?','Da. Ogled, meritve in priprava ponudbe so brezplačni in neobvezujoči.':'Yes. The visit, measurements and quote are free and without obligation.',
'Ali izdelke po meri tudi zmontirate?':'Do you also install?','Da. Izdelek izdelamo v naši delavnici, ga pripeljemo in zmontiramo pri tebi.':'Yes. We build it in our workshop, deliver it and install it at your place.',
'Izdelujete iz jekla ali inoxa?':'Steel or stainless steel?','Oboje. Material izberemo skupaj glede na namen, videz in proračun.':'Both. We choose the material together based on use, look and budget.',
'Kje izvajate storitve?':'Where do you work?','Po vsej Sloveniji, po dogovoru tudi drugje.':'All over Slovenia, and in Austria and other countries by arrangement.',
'Pogovorimo se':'Let’s talk','Opiši, kaj potrebuješ – odgovorimo v najkrajšem času in se dogovorimo za brezplačen ogled.':'Tell us what you need – we will reply as soon as possible and arrange a free site visit.',
'Telefon':'Phone','E-pošta':'E-mail','Naslov':'Address','Zgornje Hoče 7, 2311 Hoče':'Zgornje Hoče 7, 2311 Hoče, Slovenia',
'Ime in priimek*':'Full name*','E-pošta*':'E-mail*','Zanima me':'I’m interested in','Izberi …':'Choose …',
'Dvoriščna / drsna vrata':'Driveway / sliding gate','Ograja':'Railing / fence','Stopnice':'Stairs','Pergola':'Pergola','Notranja oprema':'Furniture','Drugo':'Other',
'Sporočilo*':'Message*','Opiši projekt ali izdelek, ki te zanima …':'Describe your project …',
'Z oddajo obrazca se strinjaš, da tvoje podatke uporabimo za odgovor na povpraševanje. Več v':'By sending the form you agree that we use your details to reply to your enquiry. More in our',
'politiki zasebnosti':'privacy policy (SL)','Pošlji sporočilo':'Send message','O nas':'About',
'Steeldom je blagovna znamka podjetja ARC METAL, Blaž Bratušek s.p., Zgornje Hoče 7, 2311 Hoče · Matična št.: 9418792000 · ID za DDV: SI99750716':'Steeldom is a brand of ARC METAL, Blaž Bratušek s.p., Zgornje Hoče 7, 2311 Hoče, Slovenia · Reg. no.: 9418792000 · VAT ID: SI99750716',
'Zasebnost':'Privacy','Hiter kontakt':'Quick contact','Pokliči':'Call',
'Novo povpraševanje – steeldom.si':'Novo povpraševanje (EN) – steeldom.si',
}

def lang_switch(cur):
    items=[('sl','/','SL'),('de','/de/','DE'),('en','/en/','EN')]
    return '<div class="lang-sw">'+''.join(f'<a href="{u}" hreflang="{l}"'+(' class="on"' if l==cur else '')+f'>{t}</a>' for l,u,t in items)+'</div>'
alt='\n'.join(f'<link rel="alternate" hreflang="{l}" href="https://steeldom.si{u}">' for l,u in [('sl','/'),('de','/de/'),('en','/en/'),('x-default','/')])

def build(lang):
    h=src
    m=T.get(lang,{})
    if m:
        def txt(mt):
            s=mt.group(1); k=H.unescape(s.strip())
            if k in m:
                lead=s[:len(s)-len(s.lstrip())]; trail=s[len(s.rstrip()):]
                return '>'+lead+H.escape(m[k],quote=False)+trail+'<'
            return mt.group(0)
        h=re.sub(r'>([^<]+)<',txt,h)
        def att(mt):
            k=H.unescape(mt.group(2))
            return f'{mt.group(1)}="{H.escape(m[k])}"' if k in m else mt.group(0)
        h=re.sub(r'\b(alt|placeholder|content|aria-label|value)="([^"]*)"',att,h)
        h=h.replace('<html lang="sl">',f'<html lang="{lang}">')
        # absolute asset/page paths
        h=re.sub(r'(href|src)="(?!https?:|/|#|tel:|mailto:)([^"]+)"',lambda mt:f'{mt.group(1)}="/{mt.group(2)}"',h)
        h=h.replace('href="/index.html#','href="#')
        h=h.replace('<link rel="canonical" href="https://steeldom.si/">',f'<link rel="canonical" href="https://steeldom.si/{lang}/">')
        h=h.replace('<meta property="og:url" content="https://steeldom.si/">',f'<meta property="og:url" content="https://steeldom.si/{lang}/">')
        h=h.replace('<meta name="google-site-verification" content="20X66h9AXJq0FpiPGk2ImGsq-IJuFKPf7p-CTtQIeVg">\n','')
        h=h.replace('<a href="/#kontakt" class="fab-msg">Brezplačen ogled</a>','<a href="#kontakt" class="fab-msg">'+m['Brezplačen ogled']+'</a>')
    h=h.replace('<link rel="canonical"',alt+'\n<link rel="canonical"',1) if 'hreflang="de"' not in h else h
    h=re.sub(r'<div class="lang-sw">.*?</div>','',h)
    h=h.replace('<button class="burger"',lang_switch(lang)+'\n    <button class="burger"',1)
    return h

open('./index.html','w').write(build('sl'))
import os
for l in ('de','en'):
    os.makedirs(f'./{l}',exist_ok=True)
    out=build(l); open(f'./{l}/index.html','w').write(out)
    # report untranslated text nodes
    left=[x.strip() for x in re.findall(r'>([^<]+)<',out) if x.strip() and H.unescape(x.strip()) in T['de'] and x.strip() not in('Kontakt','Telefon','Pergola')]
    print(l,'untranslated:',left[:10])
