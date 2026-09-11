import React, { useState, useEffect } from 'react';
import { fetchTasks, optimizeBlocks } from '../api';
import TaskList from './TaskList';
import StringDiagram from './StringDiagram';

const Dashboard = () => {
  const [tasks, setTasks] = useState([]);
  const [schedule, setSchedule] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [horizon, setHorizon] = useState('weekly');

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      const data = await fetchTasks();
      setTasks(data);
    } catch (err) {
      console.error('Failed to load tasks:', err);
    }
  };

  const handleOptimize = async () => {
    setIsLoading(true);
    try {
      const result = await optimizeBlocks(horizon, 'exact');
      setSchedule(result.schedule);
    } catch (err) {
      console.error('Optimization failed:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex h-screen bg-slate-950 text-slate-100 overflow-hidden">
      <TaskList tasks={tasks} onTaskSelect={(t) => console.log('Task selected:', t)} />

      <main className="flex-1 flex flex-col relative">
        <header className="p-4 border-b border-slate-800 flex justify-between items-center bg-slate-900">
          <div>
            <h1 className="text-2xl font-bold tracking-tight">Railway Block Planner</h1>
            <p className="text-sm text-slate-400">Spatio-Temporal Optimization Engine</p>
          </div>
          <div className="flex gap-4 items-center">
            <select
              value={horizon}
              onChange={(e) => setHorizon(e.target.value)}
              className="bg-slate-800 border border-slate-700 rounded px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="weekly">Weekly Plan</option>
              <option value="monthly">Monthly Strategic</option>
            </select>
            <button
              onClick={handleOptimize}
              disabled={isLoading}
              className="bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 px-4 py-2 rounded-lg font-medium transition-colors flex items-center gap-2"
            >
              {isLoading ? 'Optimizing...' : 'Generate Plan'}
            </button>
          </div>
        </header>

        <div className="flex-1 p-6 relative">
          {schedule.length > 0 ? (
            <StringDiagram schedule={schedule} />
          ) : (
            <div className="w-full h-full flex flex-col items-center justify-center text-slate-500 border-2 border-dashed border-slate-800 rounded-xl">
              <svg className="w-12 h-12 mb-4 opacity-20" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-1.447-.894L15 7m0 10V7m0 0l-6-3" />
              </svg>
              <p className="text-lg font-medium">No plan generated yet</p>
              <p className="text-sm">Click "Generate Plan" to run the CP-SAT solver</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
