import { NextResponse } from "next/server";

const NESTJS_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:3001";

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const res = await fetch(`${NESTJS_URL}/build`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data = await res.json();
    if (!res.ok) {
      return NextResponse.json(data, { status: res.status });
    }
    return NextResponse.json(data);
  } catch (err) {
    console.error("Proxy /api/build error:", err);
    return NextResponse.json(
      { error: err instanceof Error ? err.message : "Proxy request failed" },
      { status: 500 }
    );
  }
}
