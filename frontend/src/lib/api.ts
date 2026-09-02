const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ShortenRequest {
  url: string;
  custom_id?: string | null;
  expires_in?: number | null;
}

export interface ShortenResponse {
  short_id: string;
  short_url: string;
  expires_at: string | null;
}

export interface ClickRecord {
  timestamp: string;
  referrer: string | null;
}

export interface StatsResponse {
  short_id: string;
  clicks: number;
  original_url: string;
  clicks_history: ClickRecord[];
  expired: boolean;
  expires_at: string | null;
}

export interface ErrorResponse {
  detail: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface UserResponse {
  id: number;
  email: string;
  created_at: string;
}

function getHeaders(token?: string): Record<string, string> {
  const h: Record<string, string> = { "Content-Type": "application/json" };
  if (token) h["Authorization"] = `Bearer ${token}`;
  return h;
}

export async function shortenUrl(
  url: string,
  opts?: { custom_id?: string | null; expires_in?: number | null; token?: string },
): Promise<ShortenResponse> {
  const endpoint = opts?.token ? "/shorten" : "/shorten-anon";
  const res = await fetch(`${API_URL}${endpoint}`, {
    method: "POST",
    headers: getHeaders(opts?.token),
    body: JSON.stringify({
      url,
      custom_id: opts?.custom_id || undefined,
      expires_in: opts?.expires_in || undefined,
    }),
  });
  if (!res.ok) {
    const error: ErrorResponse = await res.json().catch(() => ({ detail: "Failed to shorten URL" }));
    throw new Error(error.detail || "Failed to shorten URL");
  }
  return res.json();
}

export async function getStats(sid: string): Promise<StatsResponse> {
  const res = await fetch(`${API_URL}/stats/${sid}`);
  if (!res.ok) {
    const error: ErrorResponse = await res.json().catch(() => ({ detail: "Failed to get stats" }));
    throw new Error(error.detail || "Failed to get stats");
  }
  return res.json();
}

export function getRedirectUrl(sid: string): string {
  return `${API_URL}/${sid}`;
}

export async function register(email: string, password: string): Promise<UserResponse> {
  const res = await fetch(`${API_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) {
    const err: ErrorResponse = await res.json().catch(() => ({ detail: "Register failed" }));
    throw new Error(err.detail);
  }
  return res.json();
}

export async function login(email: string, password: string): Promise<TokenResponse> {
  const res = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) {
    const err: ErrorResponse = await res.json().catch(() => ({ detail: "Login failed" }));
    throw new Error(err.detail);
  }
  return res.json();
}

export async function deleteUrl(sid: string, token: string): Promise<void> {
  const res = await fetch(`${API_URL}/${sid}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) {
    const err: ErrorResponse = await res.json().catch(() => ({ detail: "Delete failed" }));
    throw new Error(err.detail);
  }
}
