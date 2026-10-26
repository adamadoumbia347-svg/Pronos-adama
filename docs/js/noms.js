// Générateur de noms : filtre la liste (animal, sexe, lettre, style), en tire 8 au hasard, garde les favoris
(function () {
  var bloc = document.getElementById("generateur-noms");
  if (!bloc) return;
  var noms = JSON.parse(document.getElementById("donnees-noms").textContent);
  var form = bloc.querySelector("form"), sortie = bloc.querySelector(".noms-resultat");
  var CLE = "noms-favoris";
  var lire = function () { try { return JSON.parse(localStorage.getItem(CLE)) || []; } catch (e) { return []; } };
  var ecrire = function (l) { try { localStorage.setItem(CLE, JSON.stringify(l)); } catch (e) {} };
  var esc = function (s) { return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  function favoris() {
    var l = lire();
    return l.length ? '<p class="small"><strong>❤️ Vos favoris :</strong> ' + l.map(esc).join(", ") + "</p>" : "";
  }
  function afficher(tirage) {
    var fav = lire();
    sortie.innerHTML = (tirage.length
      ? '<div class="chips noms-chips">' + tirage.map(function (x) {
          var on = fav.indexOf(x.n) !== -1;
          return '<button type="button" class="chip' + (on ? " actif" : "") + '" data-nom="' + esc(x.n) + '" aria-pressed="' + on + '">' + (on ? "❤️ " : "🤍 ") + esc(x.n) + "</button>";
        }).join("") + '</div><p class="muted small">Touchez un nom pour l\'ajouter à vos favoris. Relancez pour d\'autres idées.</p>'
      : "<p>Aucun nom ne correspond : essayez un autre style.</p>") + favoris();
  }
  form.addEventListener("submit", function (ev) {
    ev.preventDefault();
    var e = form.espece.value, s = form.sexe.value, l = form.lettre.value, st = form.style.value;
    var choix = noms.filter(function (x) {
      return x.e.indexOf(e) !== -1 && (!s || x.s === s || x.s === "u") && (!l || x.n.charAt(0) === l) && (!st || x.st === st);
    });
    for (var i = choix.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = choix[i]; choix[i] = choix[j]; choix[j] = t; }
    afficher(choix.slice(0, 8));
  });
  sortie.addEventListener("click", function (ev) {
    var b = ev.target.closest("[data-nom]");
    if (!b) return;
    var n = b.getAttribute("data-nom"), l = lire(), k = l.indexOf(n);
    if (k === -1) l.push(n); else l.splice(k, 1);
    ecrire(l);
    var on = k === -1;
    b.classList.toggle("actif", on); b.setAttribute("aria-pressed", on); b.textContent = (on ? "❤️ " : "🤍 ") + n;
    var p = sortie.querySelector("p.small:last-child");
    if (p && p.textContent.indexOf("❤️") === 0) p.remove();
    sortie.insertAdjacentHTML("beforeend", favoris());
  });
})();
