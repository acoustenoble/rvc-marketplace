const fs = require("fs");
const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
  Footer, AlignmentType, BorderStyle, WidthType, ShadingType, PageNumber, TabStopType } = require("docx");
const NAVY="1B2A4A", GOLD="B8975A", GREY="555555", CREAM="F2EFE9";
const BLL="__________________________________________________";
const ASSET="/sessions/fervent-pensive-hypatia/mnt/outputs/mandat-gestion/assets/";
const OUT="/sessions/fervent-pensive-hypatia/mnt/outputs/Formulaire_proprietaire_RVC.docx";
function t(x,o={}){return new TextRun({text:x,...o});}
function field(lbl){return new Paragraph({spacing:{after:140,line:276},children:[t(lbl+" : ",{bold:true}),t(BLL,{color:GREY})]});}
function bar(x){return new Paragraph({spacing:{before:240,after:140},shading:{type:ShadingType.CLEAR,fill:NAVY},
  border:{left:{style:BorderStyle.SINGLE,size:18,color:GOLD,space:4}},children:[t("  "+x,{bold:true,color:"FFFFFF",size:22})]});}
function check(x){return new Paragraph({spacing:{after:90,line:276},indent:{left:200},children:[t("☐  ",{size:24,color:NAVY}),t(x)]});}

const c=[];
// header band
c.push(new Paragraph({spacing:{after:120},alignment:AlignmentType.LEFT,children:[new ImageRun({type:"png",
  data:fs.readFileSync(ASSET+"logo-rvc-officiel.png"),transformation:{width:210,height:118},
  altText:{title:"RVC",description:"logo",name:"logo"}})]}));
c.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{before:60,after:40},
  children:[t("FICHE DE RENSEIGNEMENTS",{bold:true,size:40,color:NAVY})]}));
c.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:60},
  border:{bottom:{style:BorderStyle.SINGLE,size:12,color:GOLD,space:6}},
  children:[t("Mise en gestion locative — à compléter par le propriétaire",{size:22,color:GOLD,bold:true})]}));
c.push(new Paragraph({alignment:AlignmentType.CENTER,spacing:{after:160},children:[t("Document préparatoire à la rédaction du mandat de gestion. Merci de remplir lisiblement et de joindre les pièces listées en dernière page.",{italics:true,size:18,color:GREY})]}));

c.push(bar("1 — LE(S) PROPRIÉTAIRE(S) / MANDANT(S)"));
[ "Civilité, nom et prénom(s)","Date et lieu de naissance","Nationalité / profession",
  "Situation matrimoniale (et régime)","Adresse postale","Téléphone","Adresse e-mail",
  "Co-indivisaires / associés (le cas échéant)","Personne morale : dénomination, RCS, représentant" ].forEach(x=>c.push(field(x)));

c.push(bar("2 — LE BIEN À GÉRER"));
[ "Adresse complète du bien","Nature (appartement / maison / local / garage)","Étage / n° de lot(s) et tantièmes",
  "Surface habitable (m²) / nombre de pièces","Année de construction","Dépendances (cave, parking, terrain…)",
  "Équipements (cuisine, chauffage, stationnement…)","Copropriété ? Nom et coordonnées du syndic","Le bien est-il : libre / loué (si loué : depuis quand)" ].forEach(x=>c.push(field(x)));

c.push(bar("3 — CONDITIONS DE LOCATION SOUHAITÉES"));
[ "Usage (habitation nue / meublée / mixte)","Loyer mensuel souhaité (€ HC)","Charges (provision / forfait / réel)",
  "Dépôt de garantie","Date de disponibilité","Souhait d'une garantie loyers impayés (oui / non)" ].forEach(x=>c.push(field(x)));

c.push(bar("4 — COORDONNÉES BANCAIRES (REVERSEMENT DES LOYERS)"));
c.push(field("Titulaire du compte"));
c.push(field("IBAN"));
c.push(field("BIC"));
c.push(new Paragraph({spacing:{after:120},children:[t("(Joindre un RIB.)",{italics:true,size:16,color:GREY})]}));

c.push(bar("5 — PIÈCES À JOINDRE"));
c.push(new Paragraph({spacing:{after:120},children:[t("Cocher et joindre les documents suivants (selon votre situation) :",{bold:true})]}));
[ "Pièce d'identité en cours de validité (chaque propriétaire)",
  "Titre de propriété (ou attestation notariée / acte d'achat)",
  "Relevé d'identité bancaire (RIB)",
  "Dossier de diagnostics techniques (DPE, électricité, gaz, plomb, amiante, ERP…)",
  "Dernier avis de taxe foncière",
  "Règlement de copropriété et coordonnées du syndic (si copropriété)",
  "Attestation d'assurance Propriétaire Non Occupant (PNO)",
  "Bail en cours et dernier avis d'échéance / quittance (si bien déjà loué)",
  "Dernier état des lieux et coordonnées du locataire en place (si loué)",
  "Pour une SCI : statuts à jour et pièce d'identité du gérant",
  "RIB du syndic / appels de charges récents (si copropriété)",
  "Coordonnées du précédent gestionnaire (si changement de gestion)" ].forEach(x=>c.push(check(x)));

c.push(new Paragraph({spacing:{before:200,after:60},children:[t("Fait à ",{bold:true,color:NAVY}),t("______________________",{color:GREY}),t("  le ",{bold:true,color:NAVY}),t("______________________",{color:GREY})]}));
c.push(new Paragraph({spacing:{before:40},children:[t("Signature du / des propriétaire(s) :",{bold:true,color:NAVY})]}));

const footer=new Footer({children:[new Paragraph({
  border:{top:{style:BorderStyle.SINGLE,size:8,color:GOLD,space:4}},spacing:{before:40},
  tabStops:[{type:TabStopType.RIGHT,position:9026}],children:[
    t("RVC IMMOBILIER — 12 Place Carnot, 50300 Avranches — 02 33 58 08 41 — contact@rvc-immobilier.fr",{size:14,color:GREY}),
    t("\tPage ",{size:14,color:GREY}),new TextRun({children:[PageNumber.CURRENT],size:14,color:GREY}),
    t(" / ",{size:14,color:GREY}),new TextRun({children:[PageNumber.TOTAL_PAGES],size:14,color:GREY})]})]});

const doc=new Document({styles:{default:{document:{run:{font:"Century Gothic",size:20}}}},
  sections:[{properties:{page:{size:{width:11906,height:16838},margin:{top:1300,right:1440,bottom:1300,left:1440}}},
    footers:{default:footer},children:c}]});
Packer.toBuffer(doc).then(b=>{fs.writeFileSync(OUT,b);console.log("FORM written");});
