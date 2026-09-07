import { describe, it, expect, vi, beforeEach } from "vitest";
import {
  shortenUrl,
  getStats,
  getRedirectUrl,
  getAnalytics,
} from "../lib/api";

const mockFetch = vi.fn();
vi.stubGlobal("fetch", mockFetch);

describe("API Client", () => {
  beforeEach(() => {
    mockFetch.mockReset();
  });

  it("getRedirectUrl returns correct URL", () => {
    const url = getRedirectUrl("abc123");
    expect(url).toContain("/abc123");
  });

  it("shortenUrl throws on network error", async () => {
    mockFetch.mockRejectedValueOnce(new Error("Failed to fetch"));
    await expect(shortenUrl("https://example.com")).rejects.toThrow(
      "Failed to fetch"
    );
  });

  it("shortenUrl returns response on success", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        short_id: "abc",
        short_url: "http://localhost/abc",
        expires_at: null,
      }),
    });
    const result = await shortenUrl("https://example.com");
    expect(result.short_id).toBe("abc");
  });

  it("shortenUrl throws on non-OK response", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 422,
      json: async () => ({ detail: "Invalid URL" }),
    });
    await expect(shortenUrl("bad-url")).rejects.toThrow("Invalid URL");
  });

  it("getStats throws on network error", async () => {
    mockFetch.mockRejectedValueOnce(new Error("Failed to fetch"));
    await expect(getStats("abc123")).rejects.toThrow("Failed to fetch");
  });

  it("getStats returns data on success", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        short_id: "abc123",
        clicks: 5,
        original_url: "https://example.com",
        clicks_history: [],
        expired: false,
        expires_at: null,
      }),
    });
    const result = await getStats("abc123");
    expect(result.clicks).toBe(5);
  });

  it("getAnalytics throws on network error", async () => {
    mockFetch.mockRejectedValueOnce(new Error("Failed to fetch"));
    await expect(getAnalytics("abc123")).rejects.toThrow("Failed to fetch");
  });

  it("getAnalytics returns data on success", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        short_id: "abc123",
        total_clicks: 10,
        unique_referrers: 3,
        top_referrers: [{ referrer: "https://twitter.com", count: 5 }],
        clicks_by_hour: { "2026-09-01T10:00:00Z": 10 },
        recent_clicks: [],
        expired: false,
        expires_at: null,
      }),
    });
    const result = await getAnalytics("abc123");
    expect(result.total_clicks).toBe(10);
    expect(result.unique_referrers).toBe(3);
  });
});
