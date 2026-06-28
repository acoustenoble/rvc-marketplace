const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell, ImageRun,
  Header, Footer, AlignmentType, LevelFormat, BorderStyle, WidthType,
  ShadingType, PageNumber, TabStopType, PageBreak, VerticalAlign
} = require("docx");

const NAVY = "1B2A4A";
const GOLD = "B8975A";
const GREY = "555555";
const CREAM = "F2EFE9";
const BL = "________________________";
const BLL = "______________________________________________";
const ASSET = "/sessions/fervent-pensive-hypatia/mnt/outputs/mandat-gestion/assets/";
const OUT = "/sessions/fervent-pensive-hypatia/mnt/outputs/Mandat_de_gestion_RVC.docx";
const NB = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: NB, bottom: NB, left: NB, right: NB, insideHorizontal: NB, insideVertical: NB };

function t(text, opts = {}) { return new TextRun({ text, ...opts }); }
function body(children, opts = {}) {
  return new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { after: 120, line: 276 },
    children: Array.isArray(children) ? children : [t(children)], ...opts });
}
function label(lbl, fill) {
  return new Paragraph({ spacing: { after: 100, line: 276 },
    children: [t(lbl + " : ", { bold: true }), t(fill || BLL, { color: GREY })] });
}
function articleBar(text) {
  return new Paragraph({ spacing: { before: 260, after: 140 },
    shading: { type: ShadingType.CLEAR, fill: NAVY },
    border: { left: { style: BorderStyle.SINGLE, size: 18, color: GOLD, space: 4 } },
    children: [t("  " + text, { bold: true, color: "FFFFFF", size: 22 })] });
}
function bullet(children) {
  return new Paragraph({ numbering: { reference: "puces", level: 0 }, alignment: AlignmentType.JUSTIFIED,
    spacing: { after: 60, line: 264 }, children: Array.isArray(children) ? children : [t(children)] });
}
function quoteArt(children) {
  return new Paragraph({ alignment: AlignmentType.JUSTIFIED, spacing: { after: 100, line: 260 },
    indent: { left: 360 }, border: { left: { style: BorderStyle.SINGLE, size: 12, color: GOLD, space: 8 } },
    children: Array.isArray(children) ? children : [t(children)] });
}

// ======================= COVER PAGE (image pleine page) =======================
const cover = [ new Paragraph({ spacing: { before: 0, after: 0 }, alignment: AlignmentType.CENTER,
  children: [ new ImageRun({ type: "png", data: fs.readFileSync(ASSET + "page-garde.png"),
    transformation: { width: 794, height: 1123 },
    altText: { title: "Page de garde", description: "Page de garde RVC IMMOBILIER", name: "cover" } }) ] }) ];

// ======================= BODY =======================
const children = [];
children.push(articleBar("ENTRE LES SOUSSIGNÉS"));
children.push(new Paragraph({ spacing: { after: 60 }, children: [t("LE MANDANT", { bold: true, color: NAVY, size: 22 })] }));
children.push(label("Civilité, nom et prénom(s)"));
children.push(label("Né(e) le " + BL + " à " + BL + ", de nationalité", null));
children.push(label("Profession / situation matrimoniale"));
children.push(label("Demeurant"));
children.push(label("Téléphone " + BL + "     Courriel"));
children.push(new Paragraph({ spacing: { after: 120 }, children: [t("(Reproduire ce bloc pour chaque co-mandant — indivision, SCI, couple.)", { italics: true, size: 16, color: GREY })] }));
children.push(body([t("Ci-après dénommé(e) « "), t("le MANDANT", { bold: true }), t(" », d'une part,")]));

children.push(new Paragraph({ spacing: { before: 80, after: 60 }, children: [t("LE MANDATAIRE", { bold: true, color: NAVY, size: 22 })] }));
children.push(body([
  t("La société "), t("RVC IMMOBILIER", { bold: true }), t(", Société par actions simplifiée (SAS) au capital de "), t("1 500 €", { bold: true }),
  t(", dont le siège social est "), t("12 Place Carnot, 50300 AVRANCHES", { bold: true }),
  t(", immatriculée au RCS de Coutances sous le numéro "), t("100 666 650", { bold: true }),
  t(", département immobilier de l'étude de commissaires de justice, représentée par "), t("Monsieur Antoine COUSTENOBLE", { bold: true }),
  t(", en sa qualité de "), t("Président", { bold: true }), t(", ayant tous pouvoirs à l'effet des présentes."),
]));
children.push(body([
  t("Activité d'administration de biens exercée en qualité de commissaire de justice, officier ministériel : à ce titre, le mandataire "),
  t("n'est pas soumis à l'obligation de carte professionnelle", { bold: true }),
  t(" prévue par la loi n° 70-9 du 2 janvier 1970. La garantie financière des fonds détenus pour le compte des mandants et l'assurance de responsabilité civile professionnelle sont assurées par la "),
  t("Chambre Nationale des Commissaires de Justice, 44 rue de Douai, 75009 Paris", { bold: true }), t("."),
]));
children.push(body([t("Ci-après dénommé(e) « "), t("le MANDATAIRE", { bold: true }), t(" » ou « l'Agence », d'autre part,")]));
children.push(body([t("Le MANDANT confère par les présentes au MANDATAIRE, qui l'accepte, le mandat d'administrer les biens désignés ci-après.", { bold: true })]));

children.push(articleBar("ARTICLE 1 — DÉSIGNATION DES BIENS"));
children.push(label("Nature et adresse du bien"));
children.push(label("Surface habitable " + BL + " m²     Nombre de pièces principales " + BL + "     Construction", null));
children.push(label("Lot(s) de copropriété / tantièmes"));
children.push(label("Dépendances (garage, cave, terrain…)"));
children.push(label("Éléments d'équipement"));
children.push(label("Usage", "habitation exclusive  /  mixte  /  professionnel  (rayer les mentions inutiles)"));

children.push(articleBar("ARTICLE 2 — CONDITIONS DE LA LOCATION"));
children.push(label("Régime juridique", "bail loi n° 89-462 du 6 juillet 1989 (nu)  /  meublé  /  autre : " + BL));
children.push(label("Durée du bail"));
children.push(label("Loyer mensuel initial " + BL + " € HC, payable d'avance le " + BL + " de chaque mois", null));
children.push(label("Charges", "provisions avec régularisation annuelle  /  forfait  /  réel"));
children.push(body([t("Révision : indexation annuelle sur l'indice de référence des loyers (IRL) publié par l'INSEE.")]));
children.push(label("Dépôt de garantie", BL + " €"));

children.push(articleBar("ARTICLE 3 — DURÉE DU MANDAT"));
children.push(body([t("Le présent mandat est donné pour une durée initiale de "), t(BL, { color: GREY }),
  t(" à compter de sa signature. Il se renouvelle ensuite par tacite reconduction par périodes de même durée, sans que sa durée totale ne puisse excéder trente ans. Chaque partie peut y mettre fin pour le terme de chaque période en avisant l'autre par lettre recommandée avec accusé de réception, moyennant un préavis de "),
  t(BL, { color: GREY }), t(" courant à compter de la première présentation de la lettre.")]));
children.push(body("Par dérogation expresse à l'article 2003 du Code civil, le décès du MANDANT n'emporte pas la résiliation de plein droit du mandat, lequel se poursuit avec ses ayants droit."));
children.push(body("En application de l'article L. 215-4 du Code de la consommation, les articles L. 215-1 à L. 215-3 et L. 241-3 du même code sont reproduits ci-après :"));
children.push(quoteArt([t("Art. L. 215-1. ", { bold: true }), t("Pour les contrats de prestations de services conclus pour une durée déterminée avec une clause de reconduction tacite, le professionnel prestataire de services informe le consommateur par écrit, par lettre nominative ou courrier électronique dédiés, au plus tôt trois mois et au plus tard un mois avant le terme de la période autorisant le rejet de la reconduction, de la possibilité de ne pas reconduire le contrat qu'il a conclu avec une clause de reconduction tacite. Cette information, délivrée dans des termes clairs et compréhensibles, mentionne, dans un encadré apparent, la date limite de non-reconduction. Lorsque cette information ne lui a pas été adressée conformément au premier alinéa, le consommateur peut mettre gratuitement un terme au contrat à tout moment à compter de la date de reconduction. Les avances effectuées après la dernière date de reconduction ou, s'agissant des contrats à durée indéterminée, après la date de transformation du contrat initial à durée déterminée, sont dans ce cas remboursées dans un délai de trente jours à compter de la date de résiliation, déduction faite des sommes correspondant, jusqu'à celle-ci, à l'exécution du contrat.", { size: 18 })]));
children.push(quoteArt([t("Art. L. 215-2. ", { bold: true }), t("Les dispositions du présent chapitre ne sont pas applicables aux exploitants des services d'eau potable et d'assainissement.", { size: 18 })]));
children.push(quoteArt([t("Art. L. 215-3. ", { bold: true }), t("Les dispositions du présent chapitre sont également applicables aux contrats conclus entre des professionnels et des non-professionnels.", { size: 18 })]));
children.push(quoteArt([t("Art. L. 241-3. ", { bold: true }), t("Lorsque le professionnel n'a pas procédé au remboursement dans les conditions prévues à l'article L. 215-1, les sommes dues sont productives d'intérêts au taux légal.", { size: 18 })]));

children.push(articleBar("ARTICLE 4 — DÉCLARATIONS ET OBLIGATIONS DU MANDANT"));
children.push(body("Le MANDANT déclare avoir la capacité juridique de disposer des biens et ne faire l'objet d'aucune mesure restreignant sa capacité à agir (tutelle, curatelle, etc.). Il s'engage à informer le MANDATAIRE de tout élément nouveau, juridique ou matériel, susceptible d'affecter l'exécution du mandat, et à lui communiquer sans délai tout congé reçu. Il déclare n'avoir opté pour aucun régime fiscal spécifique ni conventionnement, sauf mention contraire, et que les biens seront libres de toute occupation à la date convenue. S'il souhaite donner congé pour vente, il devra mandater expressément le MANDATAIRE à cet effet, en précisant prix et conditions. En cas de locations nouvelles, le MANDANT dispense le MANDATAIRE de l'envoi de la lettre recommandée prévue à l'article 67 du décret n° 72-678 du 20 juillet 1972, sous réserve que le détail des versements figure au compte rendu de gestion. Compte tenu de l'étendue de la mission, le MANDANT s'interdit de confier tout pouvoir concurrent à un tiers."));

children.push(articleBar("ARTICLE 5 — CONFORMITÉ AUX NORMES DE DÉCENCE"));
children.push(body("Le MANDANT reconnaît être tenu de mettre à disposition du locataire un logement décent ne portant pas atteinte à la santé et à la sécurité des occupants. Si le logement ne répond pas aux normes de décence et d'habitabilité en vigueur, il s'engage à réaliser les travaux de mise en conformité avant la prise de possession par le locataire."));

children.push(articleBar("ARTICLE 6 — POUVOIRS DU MANDATAIRE"));
children.push(body("Le MANDANT donne au MANDATAIRE le pouvoir d'accomplir, pour son compte, tous les actes relatifs à l'administration des biens, et notamment :"));
[
  "percevoir et encaisser les loyers, charges et accessoires, dont le MANDATAIRE demeure détenteur ; percevoir le dépôt de garantie ;",
  "donner quittance, reçu et décharge, et donner mainlevée de toute saisie, opposition et cautionnement ;",
  "réviser les loyers et ajuster les provisions ; encaisser indemnités d'occupation et d'assurance ;",
  "procéder à tous règlements (charges de copropriété et, sur demande expresse du MANDANT, impositions et taxes), récupérables le cas échéant sur les locataires ;",
  "en cas de défaut de paiement, après mise en demeure et commandement de payer infructueux, engager les procédures en paiement et expulsion — le MANDATAIRE étant attaché à une étude de commissaires de justice — le cas échéant avec le concours d'un avocat dont les honoraires auront été acceptés par le MANDANT ;",
  "accepter les congés ; réaliser ou faire réaliser les états des lieux d'entrée et de sortie ;",
  "rechercher des locataires et louer aux prix, charges et conditions jugés opportuns ; mener les actions commerciales utiles à la (re)location ;",
  "sélectionner les locataires dans le strict respect de l'interdiction de toute discrimination ;",
  "faire réaliser, aux frais du MANDANT, les diagnostics imposés par la réglementation ; rédiger et signer les baux et avenants ;",
].forEach(x => children.push(bullet(x)));
children.push(bullet([t("faire exécuter, sans autorisation préalable, les réparations et travaux d'entretien courant dont le montant n'excède pas "), t("300 € TTC", { bold: true }), t(" ; au-delà de ce montant, le MANDATAIRE soumet un ou plusieurs devis à l'accord préalable du MANDANT avant exécution, sauf urgence touchant à la sécurité des occupants ou à la jouissance du bien (notamment fuite, panne de chauffage, sinistre), où il fait procéder sans délai aux mesures conservatoires nécessaires et en informe aussitôt le MANDANT ;")]));
children.push(bullet("sur demande du MANDANT, souscrire ou résilier les contrats d'assurance de gestion courante, déclarer les sinistres et percevoir les indemnités."));
children.push(body("Les frais et débours sont supportés par le MANDANT et prélevés sur les sommes détenues pour son compte, le solde restant dû étant réglé à première demande sous quinzaine."));

children.push(articleBar("ARTICLE 7 — REDDITION DES COMPTES"));
children.push(body([t("Le MANDATAIRE rend compte de sa gestion "), t("mensuellement", { bold: true }), t(" par l'envoi d'un relevé de gérance détaillant recettes et dépenses. Les comptes sont soldés chaque mois, déduction faite des frais, honoraires et avances. Le versement du solde au MANDANT s'effectue par virement bancaire sur le compte bancaire communiqué par le MANDANT.")]));

// ===== ARTICLE 8 — RÉMUNÉRATION (TABLEAU) =====
children.push(articleBar("ARTICLE 8 — HONORAIRES DU MANDATAIRE"));
children.push(body([t("Les honoraires ci-dessous s'entendent au taux de TVA en vigueur (20 %) ; toute évolution du taux leur est immédiatement appliquée.")]));

const hb = { style: BorderStyle.SINGLE, size: 4, color: "BBBBBB" };
const hborders = { top: hb, bottom: hb, left: hb, right: hb };
function hCell(text, w, opts = {}) {
  return new TableCell({ borders: hborders, width: { size: w, type: WidthType.DXA }, verticalAlign: VerticalAlign.CENTER,
    shading: opts.fill ? { type: ShadingType.CLEAR, fill: opts.fill } : undefined,
    margins: { top: 70, bottom: 70, left: 110, right: 110 },
    children: [new Paragraph({ alignment: opts.align || AlignmentType.LEFT, children: Array.isArray(text) ? text : [t(text, { color: opts.color, bold: opts.bold, size: opts.size || 18 })] })] });
}
function hRow(c1, c2, c3, opts = {}) {
  return new TableRow({ children: [hCell(c1, 3900, opts), hCell(c2, 2600, opts), hCell(c3, 2526, { ...opts, align: AlignmentType.LEFT })] });
}
const remRows = [];
remRows.push(new TableRow({ tableHeader: true, children: [
  hCell("Prestation", 3900, { fill: NAVY, color: "FFFFFF", bold: true }),
  hCell("Base de calcul", 2600, { fill: NAVY, color: "FFFFFF", bold: true }),
  hCell("Tarif RVC", 2526, { fill: NAVY, color: "FFFFFF", bold: true }),
] }));
remRows.push(hRow("Gestion courante locative", "% des sommes quittancées (loyers + charges)", "7 % HT — 8,40 % TTC", { fill: CREAM }));
remRows.push(hRow([t("Mise en location / relocation — ", {size:18}), t("part LOCATAIRE", {bold:true,size:18}), t(" (visite, dossier, rédaction du bail)", {size:18})], "€/m² de surface habitable (plafond légal)", "8,07 €/m² (non tendue) · 10,09 €/m² (tendue) · 12,10 €/m² (très tendue)"));
remRows.push(hRow([t("État des lieux d'entrée — ", {size:18}), t("part LOCATAIRE", {bold:true,size:18})], "€/m² de surface habitable (plafond légal)", "3,03 €/m²"));
remRows.push(hRow([t("Mise en location / relocation — ", {size:18}), t("part BAILLEUR", {bold:true,size:18})], "honoraires bailleur", "montant au moins équivalent à la part locataire", { fill: CREAM }));
remRows.push(hRow("Frais de constitution d'un dossier contentieux locataire", "forfait", "120 € TTC", { fill: CREAM }));
remRows.push(hRow("Gestion d'un sinistre d'assurance", "forfait", "120 € TTC"));
remRows.push(hRow("Transmission de dossier à un confrère", "forfait", "120 € TTC", { fill: CREAM }));
remRows.push(hRow("Constitution d'un dossier ANAH (subvention / conventionnement)", "forfait", "250 € TTC"));
remRows.push(hRow("Frais de demande de diagnostics", "forfait", "10 € TTC", { fill: CREAM }));
remRows.push(hRow("Suivi de travaux sur devis (hors entretien courant)", "% du montant TTC des travaux", "5 % HT"));
children.push(new Table({ width: { size: 9026, type: WidthType.DXA }, columnWidths: [3900, 2600, 2526], rows: remRows }));
children.push(new Paragraph({ spacing: { before: 80 }, children: [t("Honoraires de gestion à la charge exclusive du MANDANT, prélevés sur chaque relevé de compte. La zone de tension locative de la commune est vérifiée avant chiffrage des honoraires de location. Plafonds locatifs au barème 2026, indexés annuellement sur l'IRL — à vérifier chaque année.", { italics: true, size: 16, color: GREY })] }));
children.push(new Paragraph({ spacing: { before: 80 }, shading: { type: ShadingType.CLEAR, fill: CREAM }, border: { left: { style: BorderStyle.SINGLE, size: 14, color: GOLD, space: 6 } }, children: [t("  Toute prestation ne figurant ni au présent mandat ni au barème ci-dessus fait l'objet d'une prestation sur devis préalablement accepté par le MANDANT.", { bold: true, size: 18, color: NAVY })] }));

children.push(articleBar("ARTICLE 9 — TRANSMISSION DU MANDAT"));
children.push(body("En cas de transmission par le MANDATAIRE de son activité, le présent mandat se poursuit au profit du successeur remplissant les conditions légales d'exercice, ce que le MANDANT accepte. Le MANDANT en est avisé par LRAR dans les meilleurs délais et, au plus tard, dans les six mois ; il peut, dans le mois de la réception, résilier dans les mêmes formes, la résiliation prenant effet un mois après réception."));

children.push(articleBar("ARTICLE 10 — ENGAGEMENT DE NON-DISCRIMINATION"));
children.push(body("Les parties s'engagent à n'opposer à aucun candidat à la location un refus fondé sur un motif discriminatoire (origine, sexe, situation de famille, grossesse, apparence physique, handicap, état de santé, mœurs, orientation sexuelle, âge, opinions, activités syndicales, appartenance vraie ou supposée à une ethnie, une nation, une prétendue race ou une religion). Toute discrimination est pénalement sanctionnée. Le MANDANT s'interdit de donner au MANDATAIRE toute directive en ce sens."));

children.push(articleBar("ARTICLE 11 — NOTIFICATIONS ÉLECTRONIQUES"));
children.push(body("Le MANDANT accepte que les lettres recommandées du MANDATAIRE lui soient adressées par envoi recommandé électronique avec accusé de réception à l'adresse mail indiquée ci-avant (art. 1126 du Code civil et L. 100 du Code des postes et des communications électroniques), via un tiers de confiance agréé. Il lui appartient de vérifier ses courriers indésirables et garantit la maîtrise exclusive de son compte e-mail."));

children.push(articleBar("ARTICLE 12 — PROTECTION DES DONNÉES (RGPD)"));
children.push(body("Les données personnelles collectées sont traitées pour l'exécution du présent mandat, la gestion de la relation, le respect des obligations légales (dont la lutte contre le blanchiment) et conservées pendant la durée légale. Le MANDANT dispose d'un droit d'accès, de rectification, d'effacement et d'opposition en s'adressant à RVC IMMOBILIER, 12 Place Carnot, 50300 AVRANCHES — contact@rvc-immobilier.fr. Toute réclamation peut être portée devant la CNIL (www.cnil.fr)."));

children.push(articleBar("ARTICLE 13 — MÉDIATION DE LA CONSOMMATION"));
children.push(body("Les différends relatifs à la validité, l'interprétation, l'exécution ou la résiliation du présent contrat pourront être soumis au médiateur de la consommation (art. L. 612-1 du Code de la consommation). Le MANDANT consommateur devra au préalable justifier avoir tenté de résoudre son litige directement auprès du MANDATAIRE par une réclamation écrite adressée par lettre recommandée avec accusé de réception. Si la réponse ne le satisfait pas, ou en l'absence de réponse sous trente (30) jours, il pourra saisir gratuitement le médiateur compétent :"));
children.push(bullet([t("Nom : ", { bold: true }), t("Le Centre de la Médiation de la Consommation des Conciliateurs de Justice (CM2C)")]));
children.push(bullet([t("Adresse : ", { bold: true }), t("14 rue Saint-Jean, 75017 Paris")]));
children.push(bullet([t("Date d'obtention du label : ", { bold: true }), t("18/04/2026")]));
children.push(bullet([t("Contact : ", { bold: true }), t("cm2c@cm2c.net — www.cm2c.net")]));
children.push(body("Les parties restent libres d'accepter ou de refuser le recours à la médiation ; la solution proposée ne s'impose pas à elles."));
children.push(body("Le MANDANT est par ailleurs informé qu'il peut s'opposer à l'utilisation de ses coordonnées téléphoniques à des fins de prospection commerciale en s'inscrivant sur la liste d'opposition au démarchage téléphonique : par courrier à Worldline — Service Bloctel — CS 61311 — 41013 BLOIS Cedex, ou en ligne sur https://www.bloctel.gouv.fr."));

children.push(articleBar("ARTICLE 14 — ÉLECTION DE DOMICILE"));
children.push(body("Les parties font élection de domicile en leurs adresses respectives indiquées en tête des présentes."));

children.push(articleBar("ARTICLE 15 — SIGNATURE ÉLECTRONIQUE"));
children.push(body("Les parties conviennent que le présent mandat peut être conclu et signé sous forme électronique, au moyen d'un procédé de signature électronique conforme au règlement (UE) n° 910/2014 du 23 juillet 2014 dit « eIDAS » et aux articles 1366 et 1367 du Code civil. Le procédé mis en œuvre permet d'identifier le signataire, de garantir son consentement aux obligations qui découlent de l'acte et d'assurer l'intégrité de l'acte signé, lequel est conservé sur support durable dans des conditions de nature à en garantir l'intégrité."));
children.push(body("Les parties reconnaissent que la signature électronique ainsi apposée a la même valeur juridique que la signature manuscrite et leur est pleinement opposable. Elles acceptent que le fichier de preuve, l'horodatage et, le cas échéant, le certificat associés à la signature électronique fassent foi de leur identité, de leur consentement et de la date de signature. Un exemplaire électronique de l'acte signé est remis à chacune des parties."));
children.push(articleBar("DATE ET SIGNATURES"));
children.push(body([t("Fait à "), t(BL, { color: GREY }), t(", en deux exemplaires originaux, le "), t(BL, { color: GREY }), t(".")]));
children.push(new Paragraph({ spacing: { after: 80 }, children: [t("Mentions manuscrites : côté mandant « Lu et approuvé — Bon pour mandat » ; côté mandataire « Lu et approuvé — Bon pour acceptation de mandat ». Parapher chaque page.", { italics: true, size: 16, color: GREY })] }));
const sb = { style: BorderStyle.SINGLE, size: 4, color: "CCCCCC" };
const sbb = { top: sb, bottom: sb, left: sb, right: sb };
children.push(new Table({ width: { size: 9026, type: WidthType.DXA }, columnWidths: [4513, 4513], rows: [
  new TableRow({ children: [
    new TableCell({ borders: sbb, width: { size: 4513, type: WidthType.DXA }, shading: { type: ShadingType.CLEAR, fill: CREAM }, margins: { top: 80, bottom: 80, left: 120, right: 120 }, children: [new Paragraph({ children: [t("Pour le MANDANT", { bold: true, color: NAVY })] })] }),
    new TableCell({ borders: sbb, width: { size: 4513, type: WidthType.DXA }, shading: { type: ShadingType.CLEAR, fill: CREAM }, margins: { top: 80, bottom: 80, left: 120, right: 120 }, children: [new Paragraph({ children: [t("Pour le MANDATAIRE", { bold: true, color: NAVY })] })] }),
  ]}),
  new TableRow({ children: [
    new TableCell({ borders: sbb, width: { size: 4513, type: WidthType.DXA }, margins: { top: 80, bottom: 520, left: 120, right: 120 }, children: [new Paragraph({ children: [t("« Lu et approuvé — Bon pour mandat »", { size: 16, color: GREY })] })] }),
    new TableCell({ borders: sbb, width: { size: 4513, type: WidthType.DXA }, margins: { top: 80, bottom: 520, left: 120, right: 120 }, children: [new Paragraph({ children: [t("RVC IMMOBILIER — A. COUSTENOBLE, Président", { size: 16, color: GREY })] }), new Paragraph({ children: [t("« Lu et approuvé — Bon pour acceptation »", { size: 16, color: GREY })] })] }),
  ]}),
]}));

const header = new Header({ children: [ new Paragraph({ alignment: AlignmentType.LEFT,
  border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: GOLD, space: 4 } }, spacing: { after: 40 },
  children: [ t("RVC ", { bold: true, size: 26, color: NAVY }), t("IMMOBILIER", { bold: true, size: 26, color: GOLD }),
    t("    Commissaires de Justice · Administrateurs de biens", { size: 14, color: GREY }) ] }) ] });
const footer = new Footer({ children: [ new Paragraph({
  border: { top: { style: BorderStyle.SINGLE, size: 8, color: GOLD, space: 4 } }, spacing: { before: 40 },
  tabStops: [{ type: TabStopType.RIGHT, position: 9026 }], children: [
    t("RVC IMMOBILIER — 12 Place Carnot, 50300 Avranches — 02 33 58 08 41", { size: 14, color: GREY }),
    t("\tParaphes ____    Page ", { size: 14, color: GREY }),
    new TextRun({ children: [PageNumber.CURRENT], size: 14, color: GREY }), t(" / ", { size: 14, color: GREY }),
    new TextRun({ children: [PageNumber.TOTAL_PAGES], size: 14, color: GREY }) ] }) ] });

const pageProps = { size: { width: 11906, height: 16838 }, margin: { top: 1300, right: 1440, bottom: 1300, left: 1440 } };
const coverPageProps = { size: { width: 11906, height: 16838 }, margin: { top: 0, right: 0, bottom: 0, left: 0 } };

const doc = new Document({
  styles: { default: { document: { run: { font: "Century Gothic", size: 20 } } } },
  numbering: { config: [ { reference: "puces", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 460, hanging: 240 } } } }] } ] },
  sections: [
    { properties: { page: coverPageProps }, children: cover },
    { properties: { page: pageProps }, headers: { default: header }, footers: { default: footer }, children },
  ],
});

Packer.toBuffer(doc).then(buffer => { fs.writeFileSync(OUT, buffer); console.log("DOCX written"); });
