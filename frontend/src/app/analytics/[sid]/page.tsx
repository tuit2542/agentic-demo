"use client";

import { useEffect, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { getAnalytics, type AnalyticsResponse } from "../../../lib/api";
import ClicksByHourChart from "../../../components/ClicksByHourChart";
import TopReferrers from "../../../components/TopReferrers";
import RecentClicks from "../../../components/RecentClicks";

export default function AnalyticsPage() {
  const params = useSearchParams();
  const router = useRouter();
  const sid = params.get("sid");
  const [data, setData] = useState<AnalyticsResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!sid) {
      setError("No short ID provided");
      setLoading(false);
      return;
    }
    getAnalytics(sid)
      .then(setData)
      .catch((e) => setError(e instanceof Error ? e.message : "Failed to load analytics"))
      .finally(() => setLoading(false));
  }, [sid]);

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <p className="text-gray-400">Loading analytics…</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <div className="text-center space-y-4">
          <p className="text-red-500 text-sm">{error}</p>
          <button onClick={() => router.back()} className="text-blue-500 underline text-sm">
            ← Back
          </button>
        </div>
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="min-h-screen p-8 max-w-4xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">
          Analytics: <span className="font-mono text-blue-500">{data.short_id}</span>
        </h1>
        <button onClick={() => router.back()} className="text-sm text-blue-500 underline">
          ← Back
        </button>
      </div>

      {/* Stat cards */}
      <div className="grid grid-cols-3 gap-4">
        <div className="border rounded-lg p-4 bg-white text-center">
          <p className="text-xs text-gray-500 uppercase">Total Clicks</p>
          <p className="text-3xl font-bold mt-1">{data.total_clicks}</p>
        </div>
        <div className="border rounded-lg p-4 bg-white text-center">
          <p className="text-xs text-gray-500 uppercase">Unique Referrers</p>
          <p className="text-3xl font-bold mt-1">{data.unique_referrers}</p>
        </div>
        <div className="border rounded-lg p-4 bg-white text-center">
          <p className="text-xs text-gray-500 uppercase">Status</p>
          <p className={`text-lg font-bold mt-1 ${data.expired ? "text-red-500" : "text-emerald-500"}`}>
            {data.expired ? "Expired" : "Active ✓"}
          </p>
        </div>
      </div>

      {/* Charts row */}
      <div className="grid grid-cols-2 gap-4">
        <TopReferrers data={data.top_referrers} />
        <ClicksByHourChart data={data.clicks_by_hour} />
      </div>

      {/* Recent clicks */}
      <RecentClicks data={data.recent_clicks} />

      {/* Expires at */}
      {data.expires_at && (
        <p className="text-xs text-gray-500">
          Expires: {new Date(data.expires_at).toLocaleString()}
        </p>
      )}
    </div>
  );
}
