"use client";

type ReferrerStat = { referrer: string | null; count: number };

export default function TopReferrers({ data }: { data: ReferrerStat[] }) {
  if (data.length === 0) {
    return (
      <div className="border rounded-lg p-4 bg-white">
        <h3 className="font-semibold mb-2">Top Referrers</h3>
        <p className="text-sm text-gray-400">No referrer data</p>
      </div>
    );
  }
  const max = Math.max(...data.map((d) => d.count), 1);
  return (
    <div className="border rounded-lg p-4 bg-white">
      <h3 className="font-semibold mb-3">Top Referrers</h3>
      <div className="space-y-2">
        {data.map((r, i) => (
          <div key={i} className="flex items-center gap-2 text-sm">
            <span className="flex-1 truncate font-mono text-xs">{r.referrer ?? "direct"}</span>
            <div className="w-24 h-4 bg-gray-100 rounded overflow-hidden">
              <div className="h-full bg-emerald-500 rounded" style={{ width: `${(r.count / max) * 100}%` }} />
            </div>
            <span className="w-6 text-right tabular-nums">{r.count}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
