/*
  STEELDOM – seznam izdelkov
  ---------------------------------------------------------------
  Vsak izdelek je en blok spodaj. Za nov izdelek kopiraj blok in spremeni podatke.

  id          kratko ime za naslov strani (male črke, brez šumnikov, z vezaji), npr. "lounge-set-milano"
  name        ime izdelka
  category    kategorija (za filtriranje), npr. "Lounge garniture"
  short       en stavek za kartico na seznamu
  description odstavki opisa
  price       cena v EUR z DDV (številka)
  oldPrice    prejšnja cena za akcijo (ali null)
  badge       kratka oznaka na kartici, npr. "Black Friday" (ali "")
  images      seznam slik v mapi img/izdelki/
  colors      izbira barv (ali [])
  specs       tabela lastnosti [ime, vrednost]
  delivery    dobavni rok
  shipping    besedilo o dostavi
  stripeLink  Stripe Payment Link (https://buy.stripe.com/...) – če je prazno, je na voljo samo predračun
  draft       true = izdelek se NE prikaže na seznamu (samo za predogled)
*/
window.STEELDOM_PRODUCTS = [
  {
    id: "primer-izdelka",
    name: "Primer izdelka – lounge garnitura",
    category: "Lounge garniture",
    short: "Testni izdelek za predogled trgovine. Zamenjamo ga s pravimi izdelki.",
    description: [
      "To je testni izdelek, s katerim preverjamo izgled strani z izdelkom. Pravi opis bo vseboval materiale, sestavo kompleta in posebnosti izdelka.",
      "Blazine so iz vodoodpornega zunanjega blaga, okvir je iz prašno barvanega aluminija ali jekla."
    ],
    price: 1290,
    oldPrice: 1490,
    badge: "Primer",
    images: [],
    colors: ["Antracit", "Bež"],
    specs: [
      ["Sestava", "kavč za 3 osebe, 2 fotelja, klubska mizica"],
      ["Mere kavča", "– × – × – cm"],
      ["Material okvirja", "–"],
      ["Blazine", "vodoodporno zunanje blago"]
    ],
    delivery: "4–6 tednov",
    shipping: "Dostava po Sloveniji vključena v ceno.",
    stripeLink: "",
    draft: true
  }
];
