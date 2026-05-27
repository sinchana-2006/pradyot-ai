/**
 * Global app state — Zustand store
 */
import { create } from 'zustand'

let _msgCounter = 0

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

  // Messages for current session — each message has a stable numeric _id
  messages: [],
  addMessage: (message) =>
    set((state) => ({
      messages: [...state.messages, { ...message, _id: ++_msgCounter }],
    })),
  clearMessages: () => set({ messages: [] }),

  // XP and gamification
  xpTotal: 0,
  addXP: (xp) => set((state) => ({ xpTotal: state.xpTotal + xp })),
}))

export default useAppStore
