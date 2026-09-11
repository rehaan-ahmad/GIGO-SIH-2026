import React from 'react';

/**
 * TaskList Component
 * Renders a vertical queue of maintenance tasks sorted by criticality.
 * Each item displays a color-coded urgency badge and basic spatial metadata.
 */
const TaskList = ({ tasks, onTaskSelect }) => {
  if (!tasks || tasks.length === 0) {
    return (
      <div className="p-4 text-gray-400 italic">
        No tasks available.
      </div>
    );
  }

  const getUrgencyColor = (score) => {
    if (score >= 80) return 'bg-red-500 text-white';
    if (score >= 50) return 'bg-amber-500 text-black';
    return 'bg-green-500 text-white';
  };

  return (
    <div className="flex flex-col h-full bg-slate-900 text-slate-100 border-r border-slate-700">
      <div className="p-4 border-b border-slate-700">
        <h2 className="text-xl font-bold">Task Queue</h2>
        <p className="text-xs text-slate-400">Sorted by Criticality Score</p>
      </div>
      <div className="flex-1 overflow-y-auto p-2 space-y-2">
        {tasks.map((task) => (
          <div
            key={task.task_id}
            onClick={() => onTaskSelect(task)}
            className="p-3 bg-slate-800 rounded-lg border border-slate-700 cursor-pointer hover:border-blue-500 transition-colors group"
          >
            <div className="flex justify-between items-start mb-1">
              <span className="text-xs font-mono text-slate-400">{task.task_id}</span>
              <span className={`text-xs px-2 py-0.5 rounded-full font-bold ${getUrgencyColor(task.criticality_score)}`}>
                {Math.round(task.criticality_score)}
              </span>
            </div>
            <div className="text-sm font-medium group-hover:text-blue-400 transition-colors">
              {task.type}
            </div>
            <div className="text-xs text-slate-500 mt-1">
              {task.dept} • {task.chainage_start_km.toFixed(2)}km - {task.chainage_end_km.toFixed(2)}km
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default TaskList;
