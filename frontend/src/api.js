import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchTasks = async () => {
  const response = await api.get('/tasks');
  return response.data;
};

export const fetchWindows = async () => {
  const response = await api.get('/windows');
  return response.data;
};

export const optimizeBlocks = async (horizon = 'weekly', mode = 'exact') => {
  const response = await api.post('/optimize-blocks', { horizon, solver_mode: mode });
  return response.data;
};

export const reoptimize = async (lockedTasks, forcedWindow, draggedTaskId) => {
  const response = await api.post('/reoptimize', {
    locked_tasks: lockedTasks,
    forced_window: forcedWindow,
    dragged_task_id: draggedTaskId,
  });
  return response.data;
};

export default api;
