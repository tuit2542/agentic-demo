"use client";

import { useState } from "react";
import { useParams } from "next/navigation";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function UnlockPage() {
  const { sid } = useParams<{ sid: string }>();
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleUnlock = async () => {
    setError(null);
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/${sid}?password=${encodeURIComponent(password)}`, {
        redirect: "manual",
      });
      if (res.status === 307) {
        const loc = res.headers.get("Location");
        if (loc) {
          // external API redirect — not a Next.js route
        
          window.location.href = loc;
        }
        return;
      }
      if (res.status === 401) {
        const data = await res.json().catch(() => ({ detail: "Invalid password" }));
        setError(data.detail);
        return;
      }
      const data = await res.json().catch(() => null);
      if (data?.detail) setError(data.detail);
      else setError("Failed to unlock");
    } catch {
      setError("Failed to unlock");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-8">
      <h1 className="text-xl font-bold mb-4">Enter password</h1>
      <p className="text-sm text-gray-500 mb-4">This link is password-protected</p>
      <div className="flex gap-2">
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          className="flex-1 border rounded px-3 py-2 text-sm"
          disabled={loading}
        />
        <button
          type="button"
          onClick={handleUnlock}
          disabled={!password || loading}
          className="bg-blue-600 text-white px-4 py-2 rounded text-sm disabled:opacity-50"
        >
          {loading ? "..." : "Unlock"}
        </button>
      </div>
      {error && <div className="text-red-500 text-sm mt-3">{error}</div>}
    </div>
  );
}