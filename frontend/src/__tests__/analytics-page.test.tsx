import { render, screen, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import AnalyticsPage from "../app/analytics/[sid]/page";

const mockFetch = vi.fn();
vi.stubGlobal("fetch", mockFetch);

// Mock next/navigation — must be before imports that use it
vi.mock("next/navigation", () => ({
  useSearchParams: () => ({ get: (key: string) => (key === "sid" ? "abc123" : null) }),
  useRouter: () => ({ push: vi.fn() }),
}));

describe("AnalyticsPage", () => {
  const mockAnalytics = {
    short_id: "abc123",
    total_clicks: 42,
    unique_referrers: 8,
    top_referrers: [
      { referrer: "https://twitter.com", count: 15 },
      { referrer: "https://github.com", count: 10 },
      { referrer: null, count: 5 },
    ],
    clicks_by_hour: { "14": 5, "15": 3, "16": 2 },
    recent_clicks: [
      { timestamp: "2026-09-04T14:32:00Z", referrer: "https://twitter.com" },
      { timestamp: "2026-09-04T14:28:00Z", referrer: null },
    ],
    expired: false,
    expires_at: "2026-09-11T15:00:00Z",
  };

  beforeEach(() => {
    mockFetch.mockReset();
  });

  it("shows loading state initially", () => {
    mockFetch.mockImplementation(() => new Promise(() => {}));
    render(<AnalyticsPage />);
    expect(screen.getByText(/Loading/i)).toBeDefined();
  });

  it("renders analytics data after fetch", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockAnalytics,
    });
    render(<AnalyticsPage />);
    await waitFor(() => {
      expect(screen.getByText("abc123")).toBeDefined();
      expect(screen.getByText("42")).toBeDefined();
      expect(screen.getByText("8")).toBeDefined();
    });
  });

  it("shows expired status correctly", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ ...mockAnalytics, expired: true }),
    });
    render(<AnalyticsPage />);
    await waitFor(() => {
      expect(screen.getByText("Expired")).toBeDefined();
    });
  });

  it("shows expires_at date", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockAnalytics,
    });
    render(<AnalyticsPage />);
    await waitFor(() => {
      expect(screen.getByText(/Expires:/)).toBeDefined();
    });
  });

  it("shows error state when fetch fails", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      json: async () => ({ detail: "Analytics not found" }),
    });
    render(<AnalyticsPage />);
    await waitFor(() => {
      expect(screen.getByText(/Analytics not found/)).toBeDefined();
    });
  });

  it("renders top referrers", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockAnalytics,
    });
    render(<AnalyticsPage />);
    await waitFor(() => {
      expect(screen.getByText("Top Referrers")).toBeDefined();
      expect(screen.getAllByText("https://twitter.com").length).toBeGreaterThanOrEqual(1);
      expect(screen.getAllByText("https://github.com").length).toBeGreaterThanOrEqual(1);
    });
  });

  it("renders recent clicks", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockAnalytics,
    });
    render(<AnalyticsPage />);
    await waitFor(() => {
      expect(screen.getByText("Recent Clicks")).toBeDefined();
    });
  });

  it("renders clicks by hour chart", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockAnalytics,
    });
    render(<AnalyticsPage />);
    await waitFor(() => {
      expect(screen.getByText("Clicks by Hour")).toBeDefined();
    });
  });
});
