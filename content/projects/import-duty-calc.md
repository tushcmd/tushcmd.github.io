---
title: Kenya Import Duty Calculator
dek: A public tool that estimates import duty from the KRA CRSP schedules.
role: Designer and engineer
status: Public
stack: FastAPI, SQLite, Next.js
links: Code|https://github.com/tushcmd/import-duty-calc
---

## The problem

- Duty on a vehicle, motorcycle or machine is worked out from the KRA CRSP schedules.
- People want a number before they commit to a purchase, and the official route is a spreadsheet.

## The approach

- The July 2025 schedules for vehicles, motorcycles and machinery sit in a SQLite database.
- A FastAPI service computes the estimate.
- A Next.js frontend takes the item details and shows the result.

## The detail that mattered

- The first version of the formula did not match KRA's numbers.
- The missing piece was a 1.25 dealer margin factor that KRA applies as an uplift.
- With it included, results matched KRA's own Excel template to six decimal places.

## Operations

- Backend is hosted on Render.
- A GitHub Actions keepalive keeps the first request after a quiet period fast.
