import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import Home from "../app/page";

const mockFetch = vi.fn();
vi.stubGlobal("fetch", mockFetch);

describe("Home Page", () => {
  beforeEach(() => {
    mockFetch.mockReset();
  });

  // === Render tests ===

  it("renders the URL shortener form", () => {
    render(<Home />);
    expect(screen.getByText("URL Shortener")).toBeDefined();
    expect(screen.getByPlaceholderText("https://example.com/very-long-url")).toBeDefined();
    expect(screen.getByRole("button", { name: "Shorten URL" })).toBeDefined();
  });

  it("has a required URL input field", () => {
    render(<Home />);
    const input = screen.getByPlaceholderText("https://example.com/very-long-url");
    expect(input.getAttribute("type")).toBe("url");
    expect(input.getAttribute("required")).not.toBeNull();
  });

  // === User interaction tests ===

  it("shows loading state when submitting", async () => {
    mockFetch.mockImplementation(
      () =>
        new Promise((resolve) =>
          setTimeout(
            () =>
              resolve({
                ok: true,
                json: async () => ({ short_id: "abc", short_url: "http://localhost/abc" }),
              }),
            100
          )
        )
    );

    render(<Home />);
    const input = screen.getByPlaceholderText("https://example.com/very-long-url");

    fireEvent.change(input, { target: { value: "https://example.com" } });
    fireEvent.submit(input.closest("form")!);

    await waitFor(() => {
      expect(screen.getByText("Shortening...")).toBeDefined();
    });

    await waitFor(() => {
      expect(screen.getByText("Shorten URL")).toBeDefined();
    });
  });

  it("clears input after successful submission", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ short_id: "abc", short_url: "http://localhost/abc" }),
    });

    render(<Home />);
    const input = screen.getByPlaceholderText("https://example.com/very-long-url") as HTMLInputElement;

    fireEvent.change(input, { target: { value: "https://example.com" } });
    fireEvent.submit(input.closest("form")!);

    await waitFor(() => {
      expect(input.value).toBe("");
    });
  });

  it("displays shortened URL after successful submission", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({
        short_id: "abc123",
        short_url: "http://localhost/abc123",
      }),
    });

    render(<Home />);
    const input = screen.getByPlaceholderText("https://example.com/very-long-url");

    fireEvent.change(input, { target: { value: "https://example.com" } });
    fireEvent.submit(input.closest("form")!);

    await waitFor(() => {
      expect(screen.getByText("Shortened URL:")).toBeDefined();
      expect(screen.getByText("http://localhost/abc123")).toBeDefined();
    });
  });

  // === Error state tests ===

  it("shows error message on network failure", async () => {
    mockFetch.mockRejectedValueOnce(new Error("Network error"));

    render(<Home />);
    const input = screen.getByPlaceholderText("https://example.com/very-long-url");

    fireEvent.change(input, { target: { value: "https://example.com" } });
    fireEvent.submit(input.closest("form")!);

    await waitFor(() => {
      expect(screen.getByRole("alert")).toBeDefined();
      expect(screen.getByText("Network error")).toBeDefined();
    });
  });

  it("shows API error detail from response", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 422,
      json: async () => ({ detail: "Invalid URL format" }),
    });

    render(<Home />);
    const input = screen.getByPlaceholderText("https://example.com/very-long-url");

    fireEvent.change(input, { target: { value: "not-a-url" } });
    fireEvent.submit(input.closest("form")!);

    await waitFor(() => {
      expect(screen.getByText("Invalid URL format")).toBeDefined();
    });
  });

  it("shows generic error when API returns non-JSON", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 500,
      json: async () => {
        throw new Error("Invalid JSON");
      },
    });

    render(<Home />);
    const input = screen.getByPlaceholderText("https://example.com/very-long-url");

    fireEvent.change(input, { target: { value: "https://example.com" } });
    fireEvent.submit(input.closest("form")!);

    await waitFor(() => {
      expect(screen.getByText("Failed to shorten URL")).toBeDefined();
    });
  });

  it("shows default error when response has no detail", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 500,
      json: async () => ({}),
    });

    render(<Home />);
    const input = screen.getByPlaceholderText("https://example.com/very-long-url");

    fireEvent.change(input, { target: { value: "https://example.com" } });
    fireEvent.submit(input.closest("form")!);

    await waitFor(() => {
      expect(screen.getByText("Failed to shorten URL")).toBeDefined();
    });
  });

  it("clears previous error on new submission", async () => {
    mockFetch.mockRejectedValueOnce(new Error("First error"));
    render(<Home />);
    const input = screen.getByPlaceholderText("https://example.com/very-long-url");

    // Submit with error
    fireEvent.change(input, { target: { value: "https://example.com" } });
    fireEvent.submit(input.closest("form")!);
    await waitFor(() => {
      expect(screen.getByText("First error")).toBeDefined();
    });

    // Submit again — error should clear
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ short_id: "abc", short_url: "http://localhost/abc" }),
    });
    fireEvent.change(input, { target: { value: "https://example.org" } });
    fireEvent.submit(input.closest("form")!);

    await waitFor(() => {
      expect(screen.queryByText("First error")).toBeNull();
      expect(screen.getByText("http://localhost/abc")).toBeDefined();
    });
  });
});
