import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import ClicksByHourChart from "../components/ClicksByHourChart";

describe("ClicksByHourChart", () => {
  it("renders bars for each hour with clicks", () => {
    const data: Record<string, number> = { "14": 5, "15": 3, "16": 0 };
    render(<ClicksByHourChart data={data} />);
    expect(screen.getByText("Clicks by Hour")).toBeDefined();
    expect(screen.getByText("14:00")).toBeDefined();
    expect(screen.getByText("15:00")).toBeDefined();
    expect(screen.getByText("5")).toBeDefined();
  });

  it("shows empty state when no data", () => {
    render(<ClicksByHourChart data={{}} />);
    expect(screen.getByText(/No click data/i)).toBeDefined();
  });

  it("handles max scaling correctly", () => {
    const data: Record<string, number> = { "10": 10, "11": 5 };
    const { container } = render(<ClicksByHourChart data={data} />);
    expect(container.textContent).toContain("10");
    expect(container.textContent).toContain("5");
  });
});
