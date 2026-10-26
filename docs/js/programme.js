// Programme « 30 jours avec mon chiot » : cases cochées gardées sur l'appareil (localStorage)
(function () {
  var cases = [].slice.call(document.querySelectorAll(".jours input[data-jour]"));
  if (!cases.length) return;
  var CLE = "programme-chiot-30";
  var lire = function () { try { return JSON.parse(localStorage.getItem(CLE)) || {}; } catch (e) { return {}; } };
  var ecrire = function (o) { try { localStorage.setItem(CLE, JSON.stringify(o)); } catch (e) {} };
  var etat = lire();
  function maj() {
    var n = cases.filter(function (c) { return c.checked; }).length;
    document.getElementById("prog-texte").textContent = n + " / " + cases.length + " jours" + (n === cases.length ? " 🎉" : "");
    document.getElementById("prog-barre").style.width = (n / cases.length * 100) + "%";
    cases.forEach(function (c) { c.closest(".jour").classList.toggle("fait", c.checked); });
  }
  cases.forEach(function (c) {
    c.checked = !!etat[c.getAttribute("data-jour")];
    c.addEventListener("change", function () {
      etat[c.getAttribute("data-jour")] = c.checked; ecrire(etat); maj();
    });
  });
  document.getElementById("prog-raz").addEventListener("click", function () {
    if (!confirm("Effacer votre progression ?")) return;
    etat = {}; ecrire(etat); cases.forEach(function (c) { c.checked = false; }); maj();
  });
  maj();
})();
