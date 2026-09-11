import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Fetches all maintenance tasks ranked by criticality.
 */
export const fetchTasks = async () => {
  const response = await api.get('/tasks');
  return response.data;
};

/**
 * Fetches all currently available corridor windows.
 */
export const fetchWindows = async () => {
  const response = await api.get('/windows');
  return response.data;
};

/**
 * Triggers the full optimization pipeline to generate a new block plan.
 */
export const optimizeBlocks = async (horizon = 'weekly', mode = 'exact') => {
  const response = await api.post('/optimize-blocks', { horizon, solver_mode: mode });
  return response.data;
};

/**
 * Triggers a real-time heuristic re-optimization for UI drag-and-drop interactions.
 */
export const reoptimize = async (lockedTasks, forcedWindow, draggedTaskId) => {
  const response = await api.post('/reoptimize', {
    locked_tasks: lockedTasks,
    forced_window: forcedWindow,
    dragged_task_id: draggedTaskId,
  });
  return response.data;
};

export default api;
