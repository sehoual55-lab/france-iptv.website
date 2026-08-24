(function(){
  'use strict';
  var $  = function(s,c){ return (c||document).querySelector(s); };
  var $$ = function(s,c){ return Array.prototype.slice.call((c||document).querySelectorAll(s)); };

  /* ---------- year ---------- */
  var yr = $('#yr'); if(yr) yr.textContent = new Date().getFullYear();

  /* ---------- sticky header ---------- */
  var hdr = $('#hdr');
  var onScroll = function(){
    if(hdr) hdr.classList.toggle('is-stuck', window.scrollY > 24);
    spy();
  };

  /* ---------- scroll spy ---------- */
  var links = $$('.nav a[href^="#"]');
  var spy = function(){
    var y = window.scrollY + 130, cur = null;
    links.forEach(function(a){
      var sec = document.getElementById(a.getAttribute('href').slice(1));
      if(sec && sec.offsetTop <= y) cur = a;
    });
    links.forEach(function(a){ a.classList.toggle('is-active', a === cur); });
  };
  window.addEventListener('scroll', onScroll, {passive:true});
  onScroll();

  /* ---------- mobile menu ---------- */
  var burger = $('#burger'), mnav = $('#mnav'), waWrap = $('#wa');
  var setMenu = function(open){
    if(!burger || !mnav) return;
    burger.classList.toggle('is-open', open);
    mnav.classList.toggle('is-open', open);
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    document.body.style.overflow = open ? 'hidden' : '';
    if(waWrap) waWrap.style.display = open ? 'none' : '';   /* never cover the menu */
  };
  if(burger) burger.addEventListener('click', function(){ setMenu(!mnav.classList.contains('is-open')); });
  $$('#mnav a').forEach(function(a){ a.addEventListener('click', function(){ setMenu(false); }); });

  /* ---------- reveal on scroll ---------- */
  if('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
    }, {rootMargin:'0px 0px -8% 0px', threshold:.08});
    $$('.rv').forEach(function(el, i){ el.style.transitionDelay = (Math.min(i,6) * 40) + 'ms'; io.observe(el); });
  } else {
    $$('.rv').forEach(function(el){ el.classList.add('in'); });
  }

  /* ---------- FAQ accordion ---------- */
  $$('.acc').forEach(function(acc){
    var q = $('.acc__q', acc), panel = $('.acc__a', acc);
    if(!q || !panel) return;
    q.addEventListener('click', function(){
      var open = acc.classList.contains('is-open');
      $$('.acc.is-open').forEach(function(o){
        o.classList.remove('is-open');
        $('.acc__a', o).style.maxHeight = '';
        $('.acc__q', o).setAttribute('aria-expanded','false');
      });
      if(!open){
        acc.classList.add('is-open');
        panel.style.maxHeight = panel.scrollHeight + 'px';
        q.setAttribute('aria-expanded','true');
      }
    });
  });

  /* ============================================================
     COMMANDE — WhatsApp uniquement. Pas de formulaire, pas de
     page de paiement, aucune donnée personnelle collectée ici.
     ============================================================ */
  var WA_PHONE = '16728962871';

  var PLANS = {
    bronze:    {name:'Bronze',    months:12, bonus:0, price:39.99},
    gold:      {name:'Gold',      months:15, bonus:3, price:49.99},
    platinum:  {name:'Platinum',  months:15, bonus:3, price:59.99},
    exclusive: {name:'Exclusive', months:24, bonus:3, price:84.99}
  };
  var EXTRA = 0.85;   /* chaque connexion supplémentaire : -15 % */
  var MAXQ  = 5;      /* connexions maximum */

  var totalFor = function(base, qty){ return base * (1 + EXTRA * (qty - 1)); };
  var eur      = function(n){ return n.toFixed(2).replace('.', ',') + ' €'; };
  var termLabel = function(p){ return p.months + ' mois' + (p.bonus ? ' +' + p.bonus + ' offerts' : ''); };

  var waOrderUrl = function(key, qty){
    var p = PLANS[key]; if(!p) return 'https://wa.me/' + WA_PHONE;
    var t = totalFor(p.price, qty);
    var txt = 'Bonjour, je suis intéressé par l\'offre ' + p.name + ' (' + termLabel(p) + ') avec '
            + qty + ' connexion' + (qty === 1 ? '' : 's')
            + ' — total ' + t.toFixed(2).replace('.', ',') + ' EUR. Merci de m\'envoyer les détails.';
    return 'https://wa.me/' + WA_PHONE + '?text=' + encodeURIComponent(txt);
  };

  /* ---------- compteur de connexions sur chaque offre ---------- */
  var CARDS = {};   /* clé -> { qty: n } , lu par la fenêtre de commande */

  $$('.plan[data-card]').forEach(function(cardEl){
    var key   = cardEl.dataset.card;
    var base  = PLANS[key].price;
    var state = CARDS[key] = {qty:1};
    var out   = $('[data-price]', cardEl);
    var qOut  = $('[data-qty]', cardEl);
    var qLab  = $('[data-qtylabel]', cardEl);
    var minus = $('[data-step="-1"]', cardEl);
    var plus  = $('[data-step="1"]', cardEl);
    var link  = $('[data-buy]', cardEl);

    var paint = function(){
      out.textContent  = eur(totalFor(base, state.qty));
      qOut.textContent = state.qty;
      qLab.textContent = state.qty === 1 ? 'connexion' : 'connexions';
      minus.disabled = state.qty <= 1;
      plus.disabled  = state.qty >= MAXQ;
      /* le lien reste un vrai lien WhatsApp : il fonctionne même sans JavaScript */
      if(link) link.href = waOrderUrl(key, state.qty);
    };
    minus.addEventListener('click', function(){ if(state.qty > 1){ state.qty--; paint(); } });
    plus .addEventListener('click', function(){ if(state.qty < MAXQ){ state.qty++; paint(); } });
    paint();
  });

  /* ============================================================
     FENÊTRE DE COMMANDE (checkout)
     Aucun numéro de carte n'est demandé ni traité sur ce site :
     le formulaire ne recueille que le nom, l'e-mail, le téléphone
     et le mode de paiement souhaité (carte bancaire ou PayPal).

     ENREGISTREMENT DES COMMANDES
     Chaque commande est ajoutée à votre Google Sheet et vous est
     envoyée par e-mail, via un script Google Apps Script déployé
     en « application web ». Collez ci-dessous l'URL /exec que
     Google vous donne à la fin du déploiement (voir le README,
     section 5b — le code du script est dans _build/google-sheet/).

     Si l'URL est vide, ou si l'envoi échoue, la commande part
     quand même sur WhatsApp : vous ne perdez jamais une vente.
     ============================================================ */
  var ORDER_ENDPOINT = 'https://script.google.com/macros/s/AKfycbwA3HmyJoR_SijlkVSNFL6JpV4i0e1uhZIUj6AgS6YfTyRDryjDQBpfqbNs8G0eH7qN/exec';
  var ORDER_TOKEN    = 'fr-iptv-2026';        /* doit être identique à TOKEN dans Code.gs */

  var co       = $('#co');
  var coForm   = $('#coForm');
  var stepForm = $('[data-co-step="form"]', co);
  var stepDone = $('[data-co-step="done"]', co);
  var current  = {key:'gold', qty:1};
  var lastFocus = null;

  var planLabel = function(p){
    return p.name + ' — ' + p.months + ' mois' + (p.bonus ? ' (+' + p.bonus + ' mois offerts)' : '');
  };

  var fillSummary = function(){
    var p = PLANS[current.key];
    var t = totalFor(p.price, current.qty);
    $('[data-sum-plan]',  co).textContent = planLabel(p);
    $('[data-sum-qty]',   co).textContent = current.qty + (current.qty === 1 ? ' connexion simultanée' : ' connexions simultanées');
    $('[data-sum-total]', co).textContent = eur(t);
  };

  var openCo = function(key, qty){
    if(!co || !PLANS[key]) return;
    lastFocus = document.activeElement;
    current.key = key;
    current.qty = qty || 1;
    stepDone.hidden = true;
    stepForm.hidden = false;
    fillSummary();
    co.classList.add('is-open');
    co.setAttribute('aria-hidden','false');
    document.body.style.overflow = 'hidden';
    setTimeout(function(){ var f = $('#coName'); if(f) f.focus(); }, 60);
  };

  var closeCo = function(){
    if(!co) return;
    co.classList.remove('is-open');
    co.setAttribute('aria-hidden','true');
    document.body.style.overflow = '';
    if(lastFocus && lastFocus.focus) lastFocus.focus();
  };

  $$('[data-buy]').forEach(function(a){
    a.addEventListener('click', function(e){
      if(!co) return;                      /* sans la fenêtre, le lien WhatsApp s'ouvre */
      e.preventDefault();
      var key = a.dataset.buy;
      openCo(key, (CARDS[key] && CARDS[key].qty) || 1);
    });
  });
  $$('[data-co-close]').forEach(function(b){ b.addEventListener('click', closeCo); });

  /* ---------- validation ---------- */
  var setErr = function(input, msg){
    var box = $('[data-err-for="' + input.id + '"]', co);
    if(box){ box.textContent = msg || ''; box.classList.toggle('is-on', !!msg); }
    input.setAttribute('aria-invalid', msg ? 'true' : 'false');
  };

  var validate = function(){
    var ok = true, first = null;
    var name = $('#coName'), mail = $('#coMail'), tel = $('#coTel');

    if(name.value.trim().length < 2){ setErr(name, 'Merci d\'indiquer votre nom complet.'); ok = false; first = first || name; }
    else setErr(name, '');

    if(!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(mail.value.trim())){
      setErr(mail, 'Cette adresse e-mail ne semble pas valide.'); ok = false; first = first || mail;
    } else setErr(mail, '');

    if(tel.value.replace(/[^0-9]/g, '').length < 6){
      setErr(tel, 'Merci d\'indiquer un numéro de téléphone valide.'); ok = false; first = first || tel;
    } else setErr(tel, '');

    if(first) first.focus();
    return ok;
  };

  var orderText = function(d){
    return 'Bonjour, je souhaite commander l\'offre ' + d.plan + '.'
         + '\nConnexions : ' + d.qty
         + '\nTotal : ' + d.total
         + '\nNom : ' + d.name
         + '\nE-mail : ' + d.email
         + '\nTéléphone : ' + d.phone
         + '\nPaiement : ' + d.pay
         + '\nMerci de m\'envoyer les instructions de paiement.';
  };

  /* ---------- envoi vers Google Sheets ----------
     Encodage « form-urlencoded » volontaire : c'est une requête simple,
     donc pas de pré-vol CORS, ce que les Web Apps Apps Script ne gèrent
     pas. sendBeacon part même si l'onglet WhatsApp s'ouvre juste après ;
     fetch sert de filet quand sendBeacon n'existe pas. */
  var sendOrder = function(d){
    if(!ORDER_ENDPOINT) return;

    var f = {
      token:      ORDER_TOKEN,
      nom:        d.name,
      email:      d.email,
      telephone:  d.phone,
      formule:    d.plan,
      prix:       d.priceNum,       /* nombre brut : la colonne reste sommable */
      prix_texte: d.total,
      connexions: d.qty,
      paiement:   d.pay,
      statut:     'En attente de paiement',
      source:     'france-iptv.website'
    };

    var body = Object.keys(f).map(function(k){
      return encodeURIComponent(k) + '=' + encodeURIComponent(f[k] == null ? '' : f[k]);
    }).join('&');

    try{
      if(navigator.sendBeacon){
        var blob = new Blob([body], {type:'application/x-www-form-urlencoded;charset=UTF-8'});
        if(navigator.sendBeacon(ORDER_ENDPOINT, blob)) return;
      }
    }catch(err){}

    try{
      fetch(ORDER_ENDPOINT, {
        method:'POST', mode:'no-cors', keepalive:true,
        headers:{'Content-Type':'application/x-www-form-urlencoded;charset=UTF-8'},
        body: body
      }).catch(function(){});
    }catch(err){}
  };

  if(coForm) coForm.addEventListener('submit', function(e){
    e.preventDefault();
    if(coForm.societe && coForm.societe.value) return;     /* piège à robots */
    if(!validate()) return;

    var p    = PLANS[current.key];
    var t    = totalFor(p.price, current.qty);
    var pay  = (coForm.querySelector('input[name="paiement"]:checked') || {}).value || 'Carte bancaire';
    var data = {
      plan:     planLabel(p),
      qty:      current.qty,
      total:    eur(t),
      priceNum: t.toFixed(2),
      name:  $('#coName').value.trim(),
      email: $('#coMail').value.trim(),
      phone: $('#coDial').value + ' ' + $('#coTel').value.trim(),
      pay:   pay
    };

    var url = 'https://wa.me/' + WA_PHONE + '?text=' + encodeURIComponent(orderText(data));

    sendOrder(data);

    /* confirmation */
    $('[data-done-name]',  co).textContent = data.name.split(' ')[0];
    $('[data-done-plan]',  co).textContent = data.plan;
    $('[data-done-pay]',   co).textContent = data.pay;
    $('[data-done-total]', co).textContent = data.total;
    $('[data-done-wa]',    co).href        = url;
    stepForm.hidden = true;
    stepDone.hidden = false;
    co.querySelector('.co__panel').scrollTop = 0;

    window.open(url, '_blank', 'noopener');
  });

  /* ---------- widget WhatsApp flottant ---------- */
  var bubble = $('#waBubble'), panel = $('#waPanel'), closeBtn = $('#waClose');
  var setPanel = function(open){
    if(!panel || !bubble) return;
    panel.classList.toggle('is-open', open);
    bubble.setAttribute('aria-expanded', open ? 'true' : 'false');
  };
  if(bubble) bubble.addEventListener('click', function(){ setPanel(!panel.classList.contains('is-open')); });
  if(closeBtn) closeBtn.addEventListener('click', function(){ setPanel(false); });
  document.addEventListener('keydown', function(e){ if(e.key === 'Escape'){ setPanel(false); setMenu(false); closeCo(); } });
  document.addEventListener('click', function(e){
    if(co && co.classList.contains('is-open')) return;
    if(panel && panel.classList.contains('is-open') && !e.target.closest('#wa')) setPanel(false);
  });

  /* s'ouvre une seule fois par session, après 12 s */
  try{
    if(!sessionStorage.getItem('waSeen')){
      setTimeout(function(){
        if((!mnav || !mnav.classList.contains('is-open')) && !(co && co.classList.contains('is-open'))){
          setPanel(true);
          try{ sessionStorage.setItem('waSeen','1'); }catch(err){}
        }
      }, 12000);
    }
  }catch(err){}
})();
