import { render, screen, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import Dashboard from "../app/dashboard/page";

vi.mock("next/navigation", () => ({
  useSearchParams: () => new URLSearchParams(),
  useRouter: () => ({ push: vi.fn() }),
}));

describe("Dashboard page", () => {
  let fetchSpy: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    fetchSpy = vi.fn();
    vi.stubGlobal("fetch", fetchSpy);
    localStorage.setItem("token", "test-token");
  });

  afterEach(() => {
    localStorage.removeItem("token");
    vi.restoreAllMocks();
  });

  it("renders dashboard with user URLs", async () => {
    fetchSpy.mockResolvedValueOnce({
      ok: true,
      json: () =>
        Promise.resolve({
          urls: [
            {
              short_id: "abc123",
              original_url: "https://example.com",
              short_url: "http://localhost:8000/abc123",
              clicks: 5,
              expired: false,
              expires_at: null,
              created_at: "2026-09-07T10:00:00Z",
            },
          ],
          total: 1,
        }),
    });

    render(<Dashboard />);

    await waitFor(() => {
      expect(screen.getByText(/example\.com/)).toBeInTheDocument();
    });
    expect(screen.getByText(/abc123/)).toBeInTheDocument();
  });

  it("shows empty state when no URLs", async () => {
    fetchSpy.mockResolvedValueOnce({
      ok: true,
      json: () => Promise.resolve({ urls: [], total: 0 }),
    });

    render(<Dashboard />);

    await waitFor(() => {
      expect(screen.getByText(/No links yet/)).toBeInTheDocument();
    });
  });

  it("shows login prompt when not authenticated", async () => {
    localStorage.removeItem("token");
    render(<Dashboard />);

    await waitFor(() => {
      expect(screen.getByText(/Please log in/)).toBeInTheDocument();
    });
  });
});
