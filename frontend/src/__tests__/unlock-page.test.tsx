import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import UnlockPage from "../app/p/[sid]/page";

const mockFetch = vi.fn();
vi.stubGlobal("fetch", mockFetch);

const mockParams: { sid: string } = { sid: "test123" };

vi.mock("next/navigation", () => ({
  useParams: () => mockParams,
  useRouter: () => ({ push: vi.fn() }),
}));

describe("Password Unlock Page", () => {
  beforeEach(() => {
    mockFetch.mockReset();
    vi.clearAllMocks();
  });

  it("renders password form for protected link", async () => {
    render(<UnlockPage />);

    expect(screen.getByText(/Enter password/)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /unlock/i })).toBeInTheDocument();
  });

  it("shows error on wrong password", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 401,
      json: () => Promise.resolve({ detail: "Invalid password" }),
    });

    render(<UnlockPage />);

    const input = screen.getByPlaceholderText(/password/i);
    vi.stubGlobal("confirm", () => true);

    expect(input).toBeInTheDocument();
  });
});