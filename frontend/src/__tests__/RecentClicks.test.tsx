import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import RecentClicks from "../components/RecentClicks";

describe("RecentClicks", () => {
  const mockClicks = [
    { timestamp: "2026-09-04T14:32:00Z", referrer: "https://twitter.com" },
    { timestamp: "2026-09-04T14:28:00Z", referrer: null },
    { timestamp: "2026-09-04T14:15:00Z", referrer: "https://github.com" },
  ];

  it("renders recent clicks table with referrers", () => {
    render(<RecentClicks data={mockClicks} />);
    expect(screen.getByText("Recent Clicks")).toBeDefined();
    expect(screen.getByText("https://twitter.com")).toBeDefined();
    expect(screen.getByText("direct")).toBeDefined();
    expect(screen.getByText("https://github.com")).toBeDefined();
  });

  it("shows formatted timestamps (HH:MM)", () => {
    const { container } = render(<RecentClicks data={mockClicks} />);
    // toLocaleTimeString format varies by timezone; just check there's a time-like string
    const cells = container.querySelectorAll("td");
    const timeCells = Array.from(cells).filter((c) => /\d{1,2}:\d{2}/.test(c.textContent ?? ""));
    expect(timeCells.length).toBeGreaterThanOrEqual(3);
  });

  it("shows empty state when no clicks", () => {
    render(<RecentClicks data={[]} />);
    expect(screen.getByText(/No recent clicks/i)).toBeDefined();
  });

  it("limits display to 10 rows", () => {
    const manyClicks = Array.from({ length: 15 }, (_, i) => ({
      timestamp: `2026-09-04T${String(10 + i).padStart(2, "0")}:00:00Z`,
      referrer: null,
    }));
    const { container } = render(<RecentClicks data={manyClicks} />);
    const rows = container.querySelectorAll("tbody tr");
    expect(rows.length).toBe(10);
  });
});
