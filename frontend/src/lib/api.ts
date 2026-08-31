const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ShortenRequest {
  url: string;
}

export interface ShortenResponse {
  short_id: string;
  short_url: string;
}

export interface StatsResponse {
  short_id: string;
  clicks: number;
  original_url: string;
}

export interface ErrorResponse {
  detail: string;
}

export async function shortenUrl(url: string): Promise<ShortenResponse> {
  const res = await fetch(`${API_URL}/shorten`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });

  if (!res.ok) {
    const error: ErrorResponse = await res.json();
    throw new Error(error.detail || "Failed to shorten URL");
  }

  return res.json();
}

export async function getStats(sid: string): Promise<StatsResponse> {
  const res = await fetch(`${API_URL}/stats/${sid}`);

  if (!res.ok) {
    const error: ErrorResponse = await res.json();
    throw new Error(error.detail || "Failed to get stats");
  }

  return res.json();
}

export function getRedirectUrl(sid: string): string {
  return `${API_URL}/${sid}`;
}
