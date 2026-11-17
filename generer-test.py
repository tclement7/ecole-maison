# Génère test/index.html à partir de index.html :
# clés de stockage à part, bandeau orange fixé en haut, pas de service worker, synchro coupée, bouton « Outils ».
import sys, pathlib
src = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else 'index.html')
dst = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else 'test/index.html')
h = src.read_text(encoding='utf-8')
def rep(a, b):
    global h
    assert h.count(a) == 1, 'introuvable ou multiple : ' + a[:70]
    h = h.replace(a, b)
rep("var CLE = 'ecole-maison-v1';", "var CLE = 'ecole-maison-TEST-v1';")
rep("var SYNC_CLE = 'ecole-maison-sync'", "var SYNC_CLE = 'ecole-maison-TEST-sync'")
rep("function appelServeur(url, corps){", "function appelServeur(url, corps){ return Promise.reject(new Error('Synchronisation désactivée dans la version de test.'));")
rep("function planifierSynchro(delai){", "function planifierSynchro(delai){ return;")
rep("if ('serviceWorker' in navigator && /^https?:$/.test(location.protocol)){", "if (false){")
rep("<title>", "<title>TEST · ")
BANDEAU = '''<div id="test-bandeau" style="position:fixed;top:0;left:0;right:0;box-sizing:border-box;z-index:999;background:#FF8A00;color:#1A1740;font-weight:800;padding:6px 10px;display:flex;gap:8px;align-items:center;justify-content:space-between;font-family:inherit">
  <span>VERSION DE TEST · données séparées</span>
  <button id="test-outils" style="background:#1A1740;color:#fff;border:0;border-radius:10px;padding:6px 12px;font-weight:800">Outils</button>
</div>
<div id="test-panneau" hidden style="position:fixed;top:48px;left:0;right:0;max-width:560px;margin:6px auto;z-index:999;background:#2B2660;border:3px solid #FF8A00;border-radius:14px;padding:10px;display:grid;gap:8px">
  <button class="bouton" id="test-demo">Créer 4 enfants d'exemple (code parents 0000)</button>
  <button class="bouton second" id="test-raz">Remettre les démos à zéro</button>
  <button class="bouton second" id="test-tout">Tout effacer</button>
</div>
'''
i = h.index('<body'); j = h.index('>', i) + 1
h = h[:j] + '\n' + BANDEAU + h[j:]
OUTILS = r'''
/* ===== version de test : outils ===== */
(function(){
  var DEMO = [ ['Lina','GS','🪿'], ['Tom','CP','🐶'], ['Emma','CE2','🦛'], ['Hugo','CM1','🐘'] ];
  var LECT = { CE2:{ t:'ce2-herisson', v:[52,55,54,60,63,61,67,70] }, CM1:{ t:'cm1-phare', v:[84,88,86,91,95,94,101] } };
  var pt0 = parseFloat(getComputedStyle(document.body).paddingTop) || 0;
  function caler(){ document.body.style.paddingTop = (pt0 + $('test-bandeau').offsetHeight) + 'px'; }
  caler(); window.addEventListener('resize', caler);
  function creerDemos(){
    DEMO.forEach(function(x, k){
      var id = 'demo' + k, c = x[1];
      if (!DB.profils.some(function(p){ return p.id === id; }))
        DB.profils.push({ id:id, nom:x[0], classe:c, avatar:x[2], couleur:COULEURS_PROFIL[k % COULEURS_PROFIL.length] });
      DB.donnees[id] = vide(nivDef('arbre', c), nivDef('fractions', c)); completer(DB.donnees[id], c);
      var L = LECT[c];
      if (L){ var t = texteParId(L.t), n = nbMots(t.texte);
        L.v.forEach(function(m, i){ var d = new Date(Date.now() - (L.v.length - i) * 4 * 864e5);
          DB.donnees[id].lecture.seances.push({ date:d.toISOString(), texte:t.id, titre:t.titre, classe:t.classe, temps:60, mots:Math.min(n, m + 2), erreurs:2, mclm:m, prosodie:null, rates:[], valideMission:true }); }); }
    });
    if (!DB.codeHash) DB.codeHash = hacher('0000');
    sauver(); dessinerProfils(); montrer('s-profils');
  }
  $('test-outils').addEventListener('click', function(){ $('test-panneau').hidden = !$('test-panneau').hidden; });
  $('test-demo').addEventListener('click', function(){ creerDemos(); $('test-panneau').hidden = true; });
  $('test-raz').addEventListener('click', function(){ var b = this; confirmer(b, 'Confirmer la remise à zéro ?', function(){ creerDemos(); $('test-panneau').hidden = true; }); });
  $('test-tout').addEventListener('click', function(){ var b = this; confirmer(b, 'Confirmer : tout effacer ?', function(){
    try { localStorage.removeItem(CLE); localStorage.removeItem(SYNC_CLE); } catch(e){} location.reload(); }); });
})();
'''
rep("window.__test = {", OUTILS + "window.__test = {")
dst.parent.mkdir(parents=True, exist_ok=True)
dst.write_text(h, encoding='utf-8')
print('Version de test écrite :', dst)
