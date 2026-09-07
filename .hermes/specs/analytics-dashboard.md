# Analytics Dashboard

## User Story
เป็นผู้ใช้ URL shortener แล้วอยากดู analytics ของ link ตัวเองว่ามีคน click กี่ครั้ง, referrer อะไรบ้าง, click pattern เป็นยังไง

## Acceptance Criteria
Given ผู้ใช้缩短 link แล้วมี click data
When กดปุ่ม "Analytics" บน link ที่สร้างไว้
Then แสดง dashboard ที่มี:
- **Total clicks** — ตัวเลข total ชัดเจน
- **Unique referrers** — กี่ referrer ต่างกัน
- **Top referrers** — bar chart / table แสดง top referrers พร้อม count
- **Clicks by hour** — bar chart แสดง click pattern แต่ละชั่วโมง (24 ชั่วโมง)
- **Recent clicks** — table แสดง timestamp + referrer ของ click ล่าสุด 10 ตัว
- **Expired status** — แสดงว่า link หมดอายุหรือยัง
- **Expires at** — ถ้ามี TTL แสดงวันหมดอายุ

## UI Layout
```
┌─────────────────────────────────────────────┐
│  Analytics: abc123                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Total    │  │ Unique   │  │ Status   │  │
│  │ Clicks   │  │ Referrers│  │ Active ✓ │  │
│  │    42    │  │    8     │  │          │  │
│  └──────────┘  └──────────┘  └──────────┘  │
│                                             │
│  Top Referrers          Clicks by Hour      │
│  ┌──────────────────┐  ┌──────────────────┐ │
│  │ direct    ██████ │  │  █              │ │
│  │ twitter   ████   │  │  ██    █        │ │
│  │ github    ██     │  │  ███  ███       │ │
│  │ other     █      │  │  ██████████     │ │
│  └──────────────────┘  └──────────────────┘ │
│                                             │
│  Recent Clicks                              │
│  ┌──────────────────────────────────────┐   │
│  │ 14:32  direct          —             │   │
│  │ 14:28  twitter.com     —             │   │
│  │ 14:15  github.com      —             │   │
│  └──────────────────────────────────────┘   │
│                                             │
│  Expires: 2026-09-11 15:00                  │
│  [← Back] [Copy Link] [Delete]             │
└─────────────────────────────────────────────┘
```

## API Contract
```typescript
GET /analytics/{sid}
Response: AnalyticsResponse {
  short_id: string
  total_clicks: number
  unique_referrers: number
  top_referrers: ReferrerStat[]  // { referrer, count }
  clicks_by_hour: Record<string, number>  // "14" -> 5
  recent_clicks: ClickRecord[]  // { timestamp, referrer }
  expired: boolean
  expires_at: string | null
}
```

## Files to Modify
- `frontend/src/app/analytics/[sid]/page.tsx` — ใหม่ (Next.js dynamic route)
- `frontend/src/components/ClicksByHourChart.tsx` — bar chart component
- `frontend/src/components/TopReferrers.tsx` — referrer list
- `frontend/src/components/RecentClicks.tsx` — recent clicks table
- `frontend/src/lib/api.ts` — มี getAnalytics() แล้ว ✅

## TDD Checklist
- [ ] RED: test analytics page renders with data
- [ ] RED: test clicks by hour bar chart
- [ ] RED: test top referrers display
- [ ] RED: test recent clicks table
- [ ] RED: test expired status display
- [ ] RED: test error state when analytics fails
- [ ] GREEN: implement all components
- [ ] REFACTOR: clean up
