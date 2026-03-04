"use client";

import { useQuery } from "@tanstack/react-query";
import { apiGet } from "@/lib/api";

export function useDashboard(studentId: string, token: string) {
  return useQuery({
    queryKey: ["dashboard", studentId],
    queryFn: () => apiGet(`/analytics/dashboard/${studentId}`, token),
    staleTime: 30_000,
    refetchInterval: 60_000
  });
}
