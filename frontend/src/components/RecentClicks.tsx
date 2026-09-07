"use client";

type ClickRecord = { timestamp: string; referrer: string | null };
const MAX_ROWS = 10;

export default function RecentClicks({ data }: { data: ClickRecord[] }) {
  if (data.length === 0) {
    return (
      <div className="border rounded-lg p-4 bg-white">
        <h3 className="font-semibold mb-2">Recent Clicks</h3>
        <p className="text-sm text-gray-400">No recent clicks</p>
      </div>
    );
  }
  const shown = data.slice(0, MAX_ROWS);
  return (
    <div className="border rounded-lg p-4 bg-white">
      <h3 className="font-semibold mb-3">Recent Clicks</h3>
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b text-gray-500 text-left">
            <th className="pb-2">Time</th>
            <th className="pb-2">Referrer</th>
          </tr>
        </thead>
        <tbody>
          {shown.map((c, i) => {
            const d = new Date(c.timestamp);
            const time = d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
            return (
              <tr key={i} className="border-b last:border-0">
                <td className="py-1.5 tabular-nums">{time}</td>
                <td className="py-1.5 font-mono text-xs">{c.referrer ?? "direct"}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
