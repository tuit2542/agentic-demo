"use client";

import { useState } from "react";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Home() {
  const [url, setUrl] = useState("");
  const [customId, setCustomId] = useState("");
  const [expiresIn, setExpiresIn] = useState("");
  const [shortUrl, setShortUrl] = useState("");
  const [expiresAt, setExpiresAt] = useState<string | null>(null);
  const [shortId, setShortId] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Auth
  const [token, setToken] = useState<string | null>(() => {
    if (typeof window === "undefined") return null;
    return localStorage.getItem("token");
  });
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [authError, setAuthError] = useState("");
  const [userEmail, setUserEmail] = useState<string | null>(() => {
    if (typeof window === "undefined") return null;
    return localStorage.getItem("userEmail");
  });

  // Stats
  const [stats, setStats] = useState<{ clicks: number; expired: boolean } | null>(null);

  const doRegister = async () => {
    setAuthError("");
    try {
      const res = await fetch(`${API_URL}/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      if (!res.ok) throw new Error((await res.json()).detail || "Register failed");
      await doLogin();
    } catch (e) { setAuthError(e instanceof Error ? e.message : "Error"); }
  };

  const doLogin = async () => {
    setAuthError("");
    try {
      const res = await fetch(`${API_URL}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
      if (!res.ok) throw new Error((await res.json()).detail || "Login failed");
      const data = await res.json();
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("userEmail", email);
      setToken(data.access_token);
      setUserEmail(email);
    } catch (e) { setAuthError(e instanceof Error ? e.message : "Error"); }
  };

  const doLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("userEmail");
    setToken(null);
    setUserEmail(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(""); setShortUrl(""); setExpiresAt(null); setStats(null); setLoading(true);
    try {
      const body: Record<string, unknown> = { url };
      if (customId.trim()) body.custom_id = customId.trim();
      if (expiresIn.trim()) body.expires_in = parseInt(expiresIn, 10);
      const endpoint = token ? "/shorten" : "/shorten-anon";
      const headers: Record<string, string> = { "Content-Type": "application/json" };
      if (token) headers["Authorization"] = `Bearer ${token}`;
      const res = await fetch(`${API_URL}${endpoint}`, {
        method: "POST", headers, body: JSON.stringify(body),
      });
      if (!res.ok) throw new Error((await res.json().catch(() => ({}))).detail || "Failed to shorten URL");
      const data = await res.json();
      setShortUrl(data.short_url); setShortId(data.short_id); setExpiresAt(data.expires_at);
      setUrl("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error");
    } finally { setLoading(false); }
  };

  const fetchStats = async (sid: string) => {
    try {
      const res = await fetch(`${API_URL}/stats/${sid}`);
      if (!res.ok) throw new Error("not found");
      const d = await res.json();
      setStats({ clicks: d.clicks, expired: d.expired });
    } catch { setStats(null); }
  };

  const handleDelete = async () => {
    if (!token || !shortId) return;
    try {
      const res = await fetch(`${API_URL}/${shortId}`, { method: "DELETE", headers: { Authorization: `Bearer ${token}` } });
      if (!res.ok) throw new Error((await res.json().catch(() => ({}))).detail || "Delete failed");
      setShortUrl(""); setShortId(""); setExpiresAt(null); setStats(null);
    } catch (e) { setError(e instanceof Error ? e.message : "Error"); }
  };

  return (
    <div className="flex min-h-screen flex-col items-center p-8">
      <h1 className="text-3xl font-bold mb-4">URL Shortener</h1>

      {/* Auth bar */}
      <div className="w-full max-w-lg mb-6 p-4 border rounded-lg bg-gray-50">
        {token ? (
          <div className="flex justify-between items-center">
            <span className="text-sm">Signed in as <b>{userEmail}</b></span>
            <button onClick={doLogout} className="text-sm text-red-500 underline">Logout</button>
          </div>
        ) : (
          <>
            <p className="text-sm font-medium mb-2">Login / Register (optional — anon works too)</p>
            <div className="flex gap-2">
              <input value={email} onChange={e => setEmail(e.target.value)} placeholder="email" className="flex-1 px-3 py-1.5 border rounded text-sm" />
              <input type="password" value={password} onChange={e => setPassword(e.target.value)} placeholder="password" className="flex-1 px-3 py-1.5 border rounded text-sm" />
            </div>
            <div className="flex gap-2 mt-2">
              <button onClick={doLogin} className="px-4 py-1.5 bg-blue-500 text-white rounded text-sm">Login</button>
              <button onClick={doRegister} className="px-4 py-1.5 bg-gray-200 rounded text-sm">Register</button>
            </div>
            {authError && <p className="text-xs text-red-500 mt-1">{authError}</p>}
          </>
        )}
      </div>

      {/* Shorten form */}
      <form onSubmit={handleSubmit} className="w-full max-w-lg space-y-3">
        <input type="url" value={url} onChange={e => setUrl(e.target.value)} placeholder="https://example.com/very-long-url" required className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none" />
        <div className="flex gap-2">
          <input value={customId} onChange={e => setCustomId(e.target.value)} placeholder="custom ID (optional, 3-20 chars)" pattern="[a-zA-Z0-9_-]{3,20}" className="flex-1 px-4 py-2 border rounded-lg text-sm" />
          <select value={expiresIn} onChange={e => setExpiresIn(e.target.value)} className="px-3 py-2 border rounded-lg text-sm">
            <option value="">Never expires</option>
            <option value="3600">1 hour</option>
            <option value="86400">1 day</option>
            <option value="604800">7 days</option>
            <option value="2592000">30 days</option>
          </select>
        </div>
        <button type="submit" disabled={loading} className="w-full py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50">
          {loading ? "Shortening..." : "Shorten URL"}
        </button>
      </form>

      {error && <p className="mt-4 text-red-500 text-sm" role="alert">{error}</p>}

      {shortUrl && (
        <div className="mt-4 p-4 bg-gray-100 rounded-lg w-full max-w-lg space-y-2">
          <p className="text-sm text-gray-600">Shortened URL:</p>
          <a href={shortUrl} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline font-mono text-sm break-all">{shortUrl}</a>
          {expiresAt && <p className="text-xs text-gray-500">Expires: {new Date(expiresAt).toLocaleString()}</p>}
          <div className="flex gap-2 pt-2">
            <button onClick={() => navigator.clipboard.writeText(shortUrl)} className="px-3 py-1 bg-white border rounded text-sm">Copy</button>
            <button onClick={() => fetchStats(shortId)} className="px-3 py-1 bg-white border rounded text-sm">Stats</button>
            {token && <button onClick={handleDelete} className="px-3 py-1 bg-red-50 text-red-600 border border-red-200 rounded text-sm">Delete</button>}
          </div>
          {stats && <p className="text-xs">Clicks: {stats.clicks} {stats.expired && <span className="text-red-500">(expired)</span>}</p>}
        </div>
      )}
    </div>
  );
}
