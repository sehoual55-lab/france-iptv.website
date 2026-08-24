/**
 * ============================================================
 *  FRANCE IPTV — réception des commandes du site
 *  france-iptv.website  →  Google Sheets + e-mail
 * ============================================================
 *
 *  Ce script reçoit les commandes envoyées par la fenêtre de
 *  checkout du site, ajoute une ligne dans votre feuille de
 *  calcul et vous prévient par e-mail.
 *
 *  Installation : voir INSTALLATION.md (5 minutes).
 *
 *  ⚠️  Aucune donnée bancaire ne transite ici : le site ne
 *      demande jamais de numéro de carte. Ce script ne reçoit
 *      que le nom, l'e-mail, le téléphone, l'offre choisie et
 *      le moyen de paiement souhaité.
 */

// ------------------------------------------------------------
//  RÉGLAGES — les seules lignes à modifier
// ------------------------------------------------------------

/** Identifiant de votre feuille (entre /d/ et /edit dans l'URL). */
var SHEET_ID = '1lLcKbzQuhHccz_-k8ayCJ9J97DdR-lRJRLKdehQ7LrY';

/** Nom de l'onglet. Laissez '' pour utiliser le premier onglet. */
var SHEET_NAME = '';

/** Adresse qui reçoit une alerte à chaque commande. '' = pas d'e-mail. */
var NOTIFY_EMAIL = 'xyz905391@gmail.com';

/** Doit être identique à ORDER_TOKEN dans index.html. */
var TOKEN = 'fr-iptv-2026';

/** Statut écrit dans la colonne I pour une commande qui arrive. */
var STATUT_DEFAUT = 'En attente de paiement';

// ------------------------------------------------------------
//  POINT D'ENTRÉE
// ------------------------------------------------------------

function doPost(e) {
  try {
    var d = readPayload_(e);

    if (TOKEN && d.token !== TOKEN) {
      return json_({ ok: false, error: 'jeton invalide' });
    }
    if (!d.nom && !d.email && !d.telephone) {
      return json_({ ok: false, error: 'commande vide' });
    }

    var row = appendOrder_(d);
    notify_(d, row);
    return json_({ ok: true, ligne: row });

  } catch (err) {
    // On journalise sans jamais renvoyer d'erreur bloquante au site :
    // le client a déjà son onglet WhatsApp, inutile de l'inquiéter.
    console.error(err);
    return json_({ ok: false, error: String(err) });
  }
}

/** Ouvrir l'URL /exec dans un navigateur affiche ceci — pratique pour vérifier le déploiement. */
function doGet() {
  return json_({ ok: true, service: 'France IPTV — réception des commandes' });
}

// ------------------------------------------------------------
//  ÉCRITURE DANS LA FEUILLE
// ------------------------------------------------------------

function appendOrder_(d) {
  var ss = SpreadsheetApp.openById(SHEET_ID);
  var sheet = SHEET_NAME ? ss.getSheetByName(SHEET_NAME) : ss.getSheets()[0];
  if (!sheet) throw new Error('Onglet introuvable : ' + SHEET_NAME);

  ensureHeader_(sheet);

  // Un verrou évite deux commandes écrites sur la même ligne
  // si deux clients valident à la même seconde.
  var lock = LockService.getScriptLock();
  lock.waitLock(20000);
  try {
    sheet.appendRow([
      new Date(),                        // A · Date
      d.nom        || '',                // B · Nom
      d.email      || '',                // C · Email
      d.telephone  || '',                // D · Téléphone
      d.formule    || '',                // E · Formule
      toNumber_(d.prix),                 // F · Prix (€)
      toNumber_(d.connexions),           // G · Connexions
      d.paiement   || '',                // H · Paiement
      d.statut     || STATUT_DEFAUT      // I · Statut
    ]);

    var row = sheet.getLastRow();
    sheet.getRange(row, 1).setNumberFormat('dd/mm/yyyy hh:mm');
    sheet.getRange(row, 6).setNumberFormat('#,##0.00 €');
    return row;

  } finally {
    lock.releaseLock();
  }
}

/** Écrit la ligne d'en-tête si la feuille est encore vide. */
function ensureHeader_(sheet) {
  if (sheet.getLastRow() > 0) return;
  var head = ['Date', 'Nom', 'Email', 'Téléphone', 'Formule',
              'Prix (€)', 'Connexions', 'Paiement', 'Statut'];
  sheet.getRange(1, 1, 1, head.length)
       .setValues([head])
       .setFontWeight('bold')
       .setBackground('#D9D9D9')
       .setHorizontalAlignment('center');
  sheet.setFrozenRows(1);
}

// ------------------------------------------------------------
//  ALERTE E-MAIL
// ------------------------------------------------------------

function notify_(d, row) {
  if (!NOTIFY_EMAIL) return;

  var sujet = 'Nouvelle commande — ' + (d.formule || 'offre') + ' — ' + (d.nom || 'client');

  var lignes = [
    ['Offre',        d.formule],
    ['Connexions',   d.connexions],
    ['Total',        d.prix_texte || d.prix],
    ['Paiement',     d.paiement],
    ['Nom',          d.nom],
    ['E-mail',       d.email],
    ['Téléphone',    d.telephone],
    ['Statut',       d.statut || STATUT_DEFAUT]
  ];

  var texte = lignes.map(function (l) { return l[0] + ' : ' + (l[1] || '—'); }).join('\n')
    + '\n\nLigne ' + row + ' de la feuille :\n'
    + 'https://docs.google.com/spreadsheets/d/' + SHEET_ID + '/edit';

  var html =
    '<div style="font-family:Arial,Helvetica,sans-serif;max-width:520px">'
  +   '<h2 style="margin:0 0 4px;font-size:19px">Nouvelle commande</h2>'
  +   '<p style="margin:0 0 18px;color:#666;font-size:13px">france-iptv.website</p>'
  +   '<table cellpadding="0" cellspacing="0" style="width:100%;border-collapse:collapse;font-size:14px">'
  +     lignes.map(function (l) {
          return '<tr>'
               + '<td style="padding:9px 0;color:#666;border-bottom:1px solid #eee">' + l[0] + '</td>'
               + '<td style="padding:9px 0;text-align:right;font-weight:bold;border-bottom:1px solid #eee">'
               + escape_(l[1] || '—') + '</td></tr>';
        }).join('')
  +   '</table>'
  +   '<p style="margin:22px 0 0">'
  +     '<a href="https://docs.google.com/spreadsheets/d/' + SHEET_ID + '/edit"'
  +     ' style="background:#0B0C0E;color:#E3B23C;padding:11px 20px;border-radius:8px;'
  +     'text-decoration:none;font-weight:bold;font-size:14px">Ouvrir la feuille</a>'
  +   '</p>'
  + '</div>';

  MailApp.sendEmail({
    to: NOTIFY_EMAIL,
    subject: sujet,
    body: texte,
    htmlBody: html,
    replyTo: d.email || undefined,
    name: 'France IPTV'
  });
}

// ------------------------------------------------------------
//  OUTILS
// ------------------------------------------------------------

/**
 * Le site envoie du « form-urlencoded » (requête simple, donc
 * pas de pré-vol CORS). On accepte aussi le JSON, au cas où.
 */
function readPayload_(e) {
  if (e && e.parameter && Object.keys(e.parameter).length) return e.parameter;

  var raw = e && e.postData ? e.postData.contents : '';
  if (!raw) return {};

  if (raw.charAt(0) === '{') {
    try { return JSON.parse(raw); } catch (err) { /* on retombe plus bas */ }
  }

  var out = {};
  raw.split('&').forEach(function (pair) {
    if (!pair) return;
    var i = pair.indexOf('=');
    var k = decodeURIComponent((i < 0 ? pair : pair.slice(0, i)).replace(/\+/g, ' '));
    var v = i < 0 ? '' : decodeURIComponent(pair.slice(i + 1).replace(/\+/g, ' '));
    out[k] = v;
  });
  return out;
}

function json_(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function toNumber_(v) {
  if (v === '' || v === null || v === undefined) return '';
  var n = Number(String(v).replace(',', '.').replace(/[^0-9.\-]/g, ''));
  return isNaN(n) ? v : n;
}

function escape_(v) {
  return String(v).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

// ------------------------------------------------------------
//  TEST — lancez cette fonction une fois depuis l'éditeur pour
//  autoriser le script et vérifier que tout fonctionne.
//  Une ligne de test apparaît dans la feuille, puis supprimez-la.
// ------------------------------------------------------------

function testCommande() {
  var res = doPost({
    parameter: {
      token:      TOKEN,
      nom:        'Test Dupont',
      email:      'test@example.com',
      telephone:  '+33 6 12 34 56 78',
      formule:    'Gold — 15 mois (+3 mois offerts)',
      prix:       '134.97',
      prix_texte: '134,97 €',
      connexions: '3',
      paiement:   'PayPal',
      statut:     'TEST — à supprimer'
    }
  });
  Logger.log(res.getContent());
}
