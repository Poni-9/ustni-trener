# Ustni trener

Samostojna spletna aplikacija (PWA) za ustno učenje predmetov MAT (Matematika) in KS
(Komunikacijski sistemi), 2. letnik FE. Deluje popolnoma samostojno v brskalniku —
**brez Claude računa** in brez strežnika.

## Kaj dela

- **Vmesnik**: enak prvotni različici — dnevni cilj, oznaka "za danes/slabe/označene",
  kartice po predmetih, bralni način (preberi izrezek → skrij → vprašanje).
- **Izrezki iz dnevnega PDF-ja**: uvoz prek JSON polja ali `.json` datoteke (Več → Uvoz).
  Struktura vprašanja je ostala enaka kot prej (`id`, `subject`, `pdfRef`, `excerptText`,
  `excerptImageUrl`, `question`, `criteria`, `kind`).
- **Ponavljanje**: isti razmik ponavljanja (spaced repetition) kot prej — 0/1/3/7/16/35 dni,
  glede na oceno in uporabo namiga.
- **Shranjevanje napredka**: vse (kartice, poskusi, ocene, urnik ponovitev) se shranjuje
  v `localStorage` tega brskalnika — brez oblaka, brez prijave. V Več → Uvoz je gumb za
  **izvoz/uvoz varnostne kopije** (`.json`), ker localStorage ni sinhroniziran med napravami
  in se lahko izgubi ob brisanju podatkov brskalnika.
- **Narekovanje**: prek vgrajenega prepoznavanja govora v brskalniku (Web Speech API,
  najbolje deluje v Chrome). Brez Claude računa, a potrebuje dovoljenje za mikrofon in
  (pri Chrome) povezavo z internetom.
- **AI ocenjevanje odgovorov**: ker aplikacija ne teče več znotraj Claude.ai, nima več
  brezplačnega dostopa do modela prek Claude artifact zmogljivosti. Namesto tega kliče
  **neposredno Anthropic API** s tvojim lastnim API ključem:
  1. Ustvari ključ na [console.anthropic.com](https://console.anthropic.com/settings/keys)
     (plačuje se po dejanski porabi, groba cena nekaj centov za več deset ocenjevanj).
  2. V aplikaciji odpri **Več → Nastavitve** in vnesi ključ (shrani se samo lokalno v tem
     brskalniku, v localStorage, in gre neposredno na `api.anthropic.com` — nikamor drugam).
  3. Brez ključa aplikacija deluje naprej — kartice lahko oceniš ročno z gumbi 1–10
     (shrani se kot lastna ocena), ponavljanje in urnik delujeta enako.
  - Gumb **Preizkus AI** (Več → Preizkus AI) preveri, da klic in ocenjevanje delujeta.

## Struktura

```
index.html              # cela aplikacija (HTML + CSS + JS), brez gradnje/odvisnosti
manifest.webmanifest     # PWA manifest (ime, ikone, standalone način)
sw.js                    # service worker (osnovno predpomnjenje za delo brez interneta)
icons/                   # ikoni za domačo zaslonsko bližnjico
```

Ni potrebe po `npm install` ali gradnji — gre za statične datoteke, ki jih lahko odpreš
kar lokalno (`index.html`) ali postrežeš s katerim koli statičnim gostovanjem.

## Namestitev na telefon

Odpri objavljeno povezavo aplikacije v Chrome (Android) ali Safari (iPhone) in izberi
**"Dodaj na začetni zaslon" / "Add to Home Screen"**. Aplikacija se odpre v celozaslonskem
načinu kot prava aplikacija, ikono ima nastavljeno.

## Zasebnost podatkov

Repozitorij je zaseben. Sama aplikacija (ko je objavljena) je dostopna vsakomur s povezavo
(statično gostovanje ne pozna zasebnih repozitorijev), vendar nihče drug ne vidi tvojih
podatkov o učenju — ti so shranjeni izključno lokalno v tvojem brskalniku/napravi.
