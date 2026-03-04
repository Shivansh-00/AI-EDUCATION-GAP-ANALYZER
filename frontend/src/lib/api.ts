const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8080";

export async function apiGet(path: string, token: string) {
  const res = await fetch(`${API_BASE}${path}`, { headers: { Authorization: `Bearer ${token}` }, cache: "no-store" });
  if (!res.ok) throw new Error(`GET ${path} failed`);
  return res.json();
}

export async function apiPost(path: string, token: string, body: unknown) {
  const res = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
    body: JSON.stringify(body)
  });
  if (!res.ok) throw new Error(`POST ${path} failed`);
  return res.json();
}
