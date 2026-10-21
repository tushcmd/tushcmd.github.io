---
title: FNewsteer
dek: A loss-prevention app for traders, built around forex news blackout windows.
role: Founder and sole engineer
status: Active since March 2026
stack: FastAPI, Next.js, Expo, React Native, FastMCP
links: Live|https://fnewsteer.co; Code|https://github.com/tushcmd/fnewsteer
---

## The problem

- Price moves fast and spreads widen around scheduled high-impact news.
- Traders who miss a release time take losses they could have avoided by staying out.
- FNewsteer shows when a blackout window is open or about to open.

## What it is

One Python backend serves every surface, so a window means the same thing everywhere.

- A **FastAPI** service that owns the calendar and the blackout logic.
- A **Chrome extension** that shows the state next to the charts.
- A **React Native and Expo** app with Dashboard, Calendar and Settings tabs, onboarding and an Android home screen widget.
- A **FastMCP** server, so the same data is available inside Claude Desktop.

## The hard parts

- Metro and NativeWind configuration conflicts left the mobile app on a blank screen until resolved.
- The watchlist had to stay in sync across screens, which an in-process event bus solved.
- The Android widget rendered blank because of a misconfigured `reconfigurable` flag.
- Push notifications had to handle windows that are active now and windows about to start.

## Infrastructure

- Code lives in a uv workspace monorepo.
- Backend runs on Render from Dockerfiles built for that workspace, with a `render.yaml` Blueprint.
- GitHub Actions handle CI
- Domain is on Cloudflare.
