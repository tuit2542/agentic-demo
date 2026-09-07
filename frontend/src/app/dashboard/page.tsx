"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { getUserUrls, deleteUrl, UserUrlItem } from "../../lib/api";

export default function DashboardPage() {
  void useRouter();
  const [urls, setUrls] = useState<UserUrlItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    const stored = localStorage.getItem("token");
    if (!stored) {
      setError("Please log in");
      setLoading(false);
      return;
    }
    setToken(stored);
    setLoading(true);

    getUserUrls(stored)
      .then((res) => setUrls(res.urls))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  const handleDelete = async (sid: string) => {
    if (!token || !confirm("Delete this URL?")) return;
    try {
      await deleteUrl(sid, token);
      setUrls((prev) => prev.filter((u) => u.short_id !== sid));
    } catch (err) {
      alert("Failed to delete");
    }
  };

  if (loading) return <div className="p-8 text-center">Loading...</div>;
  if (error) return <div className="p-8 text-center text-red-500">{error}</div>;

  return (
    <div className="max-w-4xl mx-auto p-8">
      <h1 className="text-2xl font-bold mb-6">My Links</h1>
      {urls.length === 0 ? (
        <div className="text-center text-gray-500 py-12">
          No links yet.{" "}
          <Link href="/" className="text-blue-500 hover:underline">
            Create one
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {urls.map((url) => (
            <div
              key={url.short_id}
              className="border rounded-lg p-4 flex justify-between items-start"
            >
              <div className="flex-1 min-w-0">
                <div className="font-mono text-sm text-blue-600 truncate">
                  {url.short_url}
                </div>
                <div className="text-xs text-gray-500 truncate mt-1">
                  → {url.original_url}
                </div>
                <div className="text-xs text-gray-400 mt-2">
                  {url.clicks} clicks · Created {url.created_at}
                  {url.expired && (
                    <span className="ml-2 text-red-500 font-medium">Expired</span>
                  )}
                  {url.expires_at && !url.expired && (
                    <span className="ml-2 text-amber-500">
                      Expires {url.expires_at}
                    </span>
                  )}
                </div>
              </div>
              <button
                onClick={() => handleDelete(url.short_id)}
                className="ml-4 text-red-500 hover:text-red-700 text-sm"
                type="button"
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
