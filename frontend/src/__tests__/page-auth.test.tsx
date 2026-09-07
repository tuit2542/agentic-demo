import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import Home from "../app/page";

const mockFetch = vi.fn();
vi.stubGlobal("fetch", mockFetch);

describe("Auth form — flicker + usability fix", () => {
  beforeEach(() => {
    mockFetch.mockReset();
    localStorage.clear();
  });

  // RED: ปุ่ม Login/Register ต้องมี type="button" เพื่อไม่ให้ form submit แล้ว reload หน้า
  it("Login and Register buttons have type=button (prevents accidental form submit)", () => {
    render(<Home />);
    const loginBtn = screen.getByRole("button", { name: "Login" });
    const registerBtn = screen.getByRole("button", { name: "Register" });
    expect(loginBtn.getAttribute("type")).toBe("button");
    expect(registerBtn.getAttribute("type")).toBe("button");
  });

  // RED: ปุ่มต้อง disabled ตอน email/password ว่าง — กดไม่ได้เลย
  it("Login and Register buttons are disabled when inputs are empty", () => {
    render(<Home />);
    const loginBtn = screen.getByRole("button", { name: "Login" });
    const registerBtn = screen.getByRole("button", { name: "Register" });
    expect(loginBtn).toBeDisabled();
    expect(registerBtn).toBeDisabled();
  });

  // RED: พอกรอกครบทั้งสองช่อง ปุ่มต้องเปิด (enabled)
  it("buttons enable when both email and password are filled", () => {
    render(<Home />);
    fireEvent.change(screen.getByPlaceholderText("email"), { target: { value: "a@b.com" } });
    fireEvent.change(screen.getByPlaceholderText("password"), { target: { value: "secret123" } });
    expect(screen.getByRole("button", { name: "Login" })).toBeEnabled();
    expect(screen.getByRole("button", { name: "Register" })).toBeEnabled();
  });

  // RED: ปุ่มต้อง disabled ตอนกรอกแค่ email อย่างเดียว
  it("buttons stay disabled when only email is filled", () => {
    render(<Home />);
    fireEvent.change(screen.getByPlaceholderText("email"), { target: { value: "a@b.com" } });
    expect(screen.getByRole("button", { name: "Login" })).toBeDisabled();
    expect(screen.getByRole("button", { name: "Register" })).toBeDisabled();
  });

  // RED: auth error ต้องคงอยู่หลัง register fail — ไม่หายไป
  it("shows authError and it persists across re-renders", async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      json: async () => ({ detail: "Email already registered" }),
    });
    render(<Home />);
    fireEvent.change(screen.getByPlaceholderText("email"), { target: { value: "a@b.com" } });
    fireEvent.change(screen.getByPlaceholderText("password"), { target: { value: "secret123" } });
    fireEvent.click(screen.getByRole("button", { name: "Register" }));
    await waitFor(() => {
      expect(screen.getByText("Email already registered")).toBeDefined();
    });
    // wait again to confirm it doesn't flicker away
    await waitFor(() => {
      expect(screen.getByText("Email already registered")).toBeDefined();
    });
  });
});
