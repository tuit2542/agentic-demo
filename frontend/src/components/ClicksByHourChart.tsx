"use client";

type Props = { data: Record<string, number> };

export default function ClicksByHourChart({ data }: Props) {
  const entries = Object.entries(data)
    .filter(([, v]) => v > 0 || Object.keys(data).length <= 3) // show zeros when few entries
    .sort(([a], [b]) => Number(a) - Number(b));
  if (Object.keys(data).length === 0) {
    return (
      <div className="border rounded-lg p-4 bg-white">
        <h3 className="font-semibold mb-2">Clicks by Hour</h3>
        <p className="text-sm text-gray-400">No click data</p>
      </div>
    );
  }
  const max = Math.max(...Object.values(data), 1);
  return (
    <div className="border rounded-lg p-4 bg-white">
      <h3 className="font-semibold mb-3">Clicks by Hour</h3>
      <div className="space-y-2">
        {entries.map(([hour, count]) => (
          <div key={hour} className="flex items-center gap-2 text-sm">
            <span className="w-12 text-gray-500">{hour.padStart(2, "0")}:00</span>
            <div className="flex-1 h-4 bg-gray-100 rounded overflow-hidden">
              <div
                className="h-full bg-blue-500 rounded"
                style={{ width: `${(count / max) * 100}%`, minWidth: count > 0 ? "4px" : "0" }}
              />
            </div>
            <span className="w-6 text-right tabular-nums">{count}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
