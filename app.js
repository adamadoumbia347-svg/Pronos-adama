(function () {
  const pronos = (window.PRONOS || []).slice().sort((a, b) => b.date.localeCompare(a.date));
  const liens = window.LIENS || {};
  const LABELS = { en_cours: "En cours", gagne: "Gagné ✅", perdu: "Perdu ❌", rembourse: "Remboursé" };

  const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => (
    { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]
  ));
  const dateFr = (d) => new Date(d + "T12:00:00").toLocaleDateString("fr-FR", { day: "numeric", month: "short" });
  const etoiles = (n) => "★".repeat(n) + "☆".repeat(5 - n);

  // Le "jour" affiché = la date la plus récente présente dans le fichier
  const dernierJour = pronos.length ? pronos[0].date : null;
  const duJour = pronos.filter((p) => p.date === dernierJour);
  const extra = duJour.find((p) => p.extra);

  function carte(p, grande) {
    return `
      <article class="card ${grande ? "card-extra" : ""}">
        <div class="card-top">
          <span class="tag">${esc(p.sport)}</span>
          <span class="statut ${esc(p.resultat)}">${LABELS[p.resultat] || ""}</span>
        </div>
        <h3>${esc(p.match)}</h3>
        <p class="prono">${esc(p.prono)}</p>
        <div class="card-bottom">
          <span class="cote">Cote ${Number(p.cote).toFixed(2)}</span>
          <span class="etoiles" title="Confiance ${p.confiance}/5">${etoiles(p.confiance)}</span>
        </div>
        ${p.analyse ? `<p class="analyse">${esc(p.analyse)}</p>` : ""}
      </article>`;
  }

  document.getElementById("extra").innerHTML = extra
    ? carte(extra, true)
    : `<p class="vide">Pas d'Entrée Extra aujourd'hui.</p>`;

  const autres = duJour.filter((p) => p !== extra);
  document.getElementById("jour").innerHTML = autres.length
    ? autres.map((p) => carte(p, false)).join("")
    : `<p class="vide">Pas d'autres pronos aujourd'hui.</p>`;

  // Stats calculées sur les pronos terminés (mise fixe de 1 unité)
  const termines = pronos.filter((p) => p.resultat === "gagne" || p.resultat === "perdu");
  const gagnes = termines.filter((p) => p.resultat === "gagne");
  const profit = termines.reduce((s, p) => s + (p.resultat === "gagne" ? p.cote - 1 : -1), 0);
  const reussite = termines.length ? Math.round((gagnes.length / termines.length) * 100) : 0;
  const roi = termines.length ? Math.round((profit / termines.length) * 100) : 0;
  document.getElementById("stats").innerHTML = `
    <div><strong>${termines.length}</strong><span>pronos terminés</span></div>
    <div><strong>${reussite} %</strong><span>de réussite</span></div>
    <div><strong class="${roi >= 0 ? "pos" : "neg"}">${roi >= 0 ? "+" : ""}${roi} %</strong><span>rentabilité (ROI)</span></div>`;

  document.getElementById("historique").innerHTML = pronos
    .filter((p) => p.resultat !== "en_cours")
    .map((p) => `<tr>
      <td>${dateFr(p.date)}</td><td>${esc(p.match)}${p.extra ? " ⭐" : ""}</td><td>${esc(p.prono)}</td>
      <td>${Number(p.cote).toFixed(2)}</td><td class="statut ${esc(p.resultat)}">${LABELS[p.resultat]}</td></tr>`)
    .join("") || `<tr><td colspan="5" class="vide">Aucun prono terminé pour l'instant.</td></tr>`;

  // Boutons d'appel à l'action (seulement ceux qui ont un lien)
  const boutons = [
    liens.telegram && `<a class="btn" href="${esc(liens.telegram)}" target="_blank" rel="noopener">Rejoindre le Telegram</a>`,
    liens.whatsapp && `<a class="btn" href="${esc(liens.whatsapp)}" target="_blank" rel="noopener">Chaîne WhatsApp</a>`,
    liens.affiliation && `<a class="btn btn-alt" href="${esc(liens.affiliation)}" target="_blank" rel="noopener sponsored">Parier chez notre partenaire</a>`
  ].filter(Boolean);
  const cta = document.getElementById("cta");
  if (boutons.length) {
    cta.innerHTML = `<h2>Ne rate aucun prono</h2><div class="btns">${boutons.join("")}</div>`;
  } else {
    cta.remove();
  }

  document.getElementById("annee").textContent = new Date().getFullYear();
})();
