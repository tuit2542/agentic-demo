import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import TopReferrers from "../components/TopReferrers";

describe("TopReferrers", () => {
  it("renders referrer list with counts", () => {
    const data = [
      { referrer: "https://twitter.com", count: 12 },
      { referrer: null, count: 5 },
    ];
    render(<TopReferrers data={data} />);
    expect(screen.getByText("Top Referrers")).toBeDefined();
    expect(screen.getByText("https://twitter.com")).toBeDefined();
    expect(screen.getByText("direct")).toBeDefined();
    expect(screen.getByText("12")).toBeDefined();
    expect(screen.getByText("5")).toBeDefined();
  });

  it("shows empty state when no referrers", () => {
    render(<TopReferrers data={[]} />);
    expect(screen.getByText(/No referrer data/i)).toBeDefined();
  });

  it("renders bars proportional to max count", () => {
    const data = [
      { referrer: "a.com", count: 10 },
      { referrer: "b.com", count: 2 },
    ];
    const { container } = render(<TopReferrers data={data} />);
    expect(container.textContent).toContain("a.com");
    expect(container.textContent).toContain("b.com");
  });
});
