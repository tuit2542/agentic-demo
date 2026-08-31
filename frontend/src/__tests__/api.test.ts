import { describe, it, expect } from "vitest";
import { shortenUrl, getStats, getRedirectUrl } from "../lib/api";

describe("API Client", () => {
  it("getRedirectUrl returns correct URL", () => {
    const url = getRedirectUrl("abc123");
    expect(url).toContain("/abc123");
  });

  it("shortenUrl throws on network error", async () => {
    await expect(shortenUrl("https://example.com")).rejects.toThrow();
  });

  it("getStats throws on network error", async () => {
    await expect(getStats("abc123")).rejects.toThrow();
  });
});
