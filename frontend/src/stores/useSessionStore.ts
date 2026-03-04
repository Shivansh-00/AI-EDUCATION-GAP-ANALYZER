import { create } from "zustand";

type SessionState = {
  token: string;
  studentId: string;
  setSession: (token: string, studentId: string) => void;
};

export const useSessionStore = create<SessionState>((set) => ({
  token: "demo-token",
  studentId: "student-001",
  setSession: (token, studentId) => set({ token, studentId })
}));
