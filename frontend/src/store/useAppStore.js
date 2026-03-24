/**
 * Global app state — Zustand store
 * TODO (Phase 1): Expand with session state and real data
 */
import { create } from 'zustand'

const useAppStore = create((set) => ({
  // Auth
  user: null,
  setUser: (user) => set({ user }),
  clearUser: () => set({ user: null }),

  // Student profile
  profile: null,
  setProfile: (profile) => set({ profile }),

  // Current chat session
  currentSessionId: null,
  setCurrentSessionId: (id) => set({ currentSessionId: id }),

  // Messages for current session
  messages: [],
  addMessage: (message) =>
    set((state) => ({ messages: [...state.messages, message] })),
  clearMessages: () => set({ messages: [] }),

  // XP and gamification
  xpTotal: 0,
  addXP: (xp) => set((state) => ({ xpTotal: state.xpTotal + xp })),
}))

export default useAppStore
