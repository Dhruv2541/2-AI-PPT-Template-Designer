import { create } from 'zustand';

interface AppState {
  count: number;
  inc: () => void;
}

export const useStore = create<AppState>((set) => ({
  count: 1,
  inc: () => set((state) => ({ count: state.count + 1 })),
}));
