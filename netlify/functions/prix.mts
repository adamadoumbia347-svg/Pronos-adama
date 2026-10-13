import type { Config } from "@netlify/functions"

// Prix indicatif le plus bas trouvé récemment pour un trajet (données en cache Aviasales via Travelpayouts).
// Inactif tant que la variable d'environnement TRAVELPAYOUTS_TOKEN n'est pas définie dans Netlify.
// GET /api/prix?from=CDG&to=BKO&dep=2026-11-03&ret=2026-11-10

const IATA = /^[A-Z]{3}$/
const DATE = /^\d{4}-\d{2}-\d{2}$/

export default async (req: Request) => {
  const token = Netlify.env.get("TRAVELPAYOUTS_TOKEN")
  if (!token) return Response.json({ available: false }, { status: 200 })

  const q = new URL(req.url).searchParams
  const from = (q.get("from") || "").toUpperCase()
  const to = (q.get("to") || "").toUpperCase()
  const dep = q.get("dep") || ""
  const ret = q.get("ret") || ""
  if (!IATA.test(from) || !IATA.test(to) || !DATE.test(dep) || (ret && !DATE.test(ret))) {
    return Response.json({ error: "Paramètres invalides" }, { status: 400 })
  }

  const api = new URL("https://api.travelpayouts.com/aviasales/v3/prices_for_dates")
  api.search = new URLSearchParams({
    origin: from,
    destination: to,
    departure_at: dep.slice(0, 7), // le mois entier : plus de résultats en cache
    ...(ret ? { return_at: ret.slice(0, 7) } : {}),
    one_way: ret ? "false" : "true",
    sorting: "price",
    currency: "eur",
    limit: "1",
    token,
  }).toString()

  try {
    const res = await fetch(api, { headers: { "Accept-Encoding": "gzip" } })
    if (!res.ok) return Response.json({ available: false }, { status: 200 })
    const body = await res.json()
    const best = body?.data?.[0]
    if (!best) return Response.json({ available: true, price: null }, { status: 200, headers: cache() })
    return Response.json({
      available: true,
      price: best.price,
      currency: "EUR",
      airline: best.airline,
      transfers: best.transfers,
      departure_at: best.departure_at,
      return_at: best.return_at ?? null,
    }, { status: 200, headers: cache() })
  } catch {
    return Response.json({ available: false }, { status: 200 })
  }
}

const cache = () => ({ "Cache-Control": "public, max-age=3600" })

export const config: Config = { path: "/api/prix" }
