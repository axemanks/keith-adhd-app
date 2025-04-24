import { useEffect, useState } from 'react';
import './App.css';

function App() {
  // State for lists
  const [goals, setGoals] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [checkins, setCheckins] = useState([]);

  // State for forms
  const [goalTitle, setGoalTitle] = useState('');
  const [taskTitle, setTaskTitle] = useState('');
  const [checkinTaskId, setCheckinTaskId] = useState('');
  const [checkinNotes, setCheckinNotes] = useState('');

  // Fetch lists on mount
  useEffect(() => {
    fetch('/api/goals/')
      .then(async r => {
        console.log('GET /api/goals/ status:', r.status);
        const data = await r.json().catch(() => null);
        console.log('GET /api/goals/ data:', data);
        setGoals((data && data.goals) || []);
      })
      .catch(e => console.error('GET /api/goals/ error:', e));
    fetch('/api/tasks/')
      .then(async r => {
        console.log('GET /api/tasks/ status:', r.status);
        const data = await r.json().catch(() => null);
        console.log('GET /api/tasks/ data:', data);
        setTasks(data || []);
      })
      .catch(e => console.error('GET /api/tasks/ error:', e));
    fetch('/api/checkins/')
      .then(async r => {
        console.log('GET /api/checkins/ status:', r.status);
        const data = await r.json().catch(() => null);
        console.log('GET /api/checkins/ data:', data);
        setCheckins(data || []);
      })
      .catch(e => console.error('GET /api/checkins/ error:', e));
  }, []);

  // Add goal
  const handleAddGoal = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!goalTitle) return;
    const res = await fetch('/api/goals/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: goalTitle }),
    });
    if (res.ok) {
      const newGoal = await res.json();
      setGoals(g => [...g, newGoal]);
      setGoalTitle('');
    }
  };

  // Add task
  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!taskTitle) return;
    const res = await fetch('/api/tasks/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: taskTitle }),
    });
    if (res.ok) {
      const newTask = await res.json();
      setTasks(t => [...t, newTask]);
      setTaskTitle('');
    }
  };

  // Add check-in
  const handleAddCheckin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!checkinTaskId) return;
    const res = await fetch('/api/checkins/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ task_id: checkinTaskId, notes: checkinNotes }),
    });
    if (res.ok) {
      const newCheckin = await res.json();
      setCheckins(c => [...c, newCheckin]);
      setCheckinTaskId('');
      setCheckinNotes('');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 p-8">
      <main className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-8">ADHD Goals & Tasks Tracker</h1>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Goals */}
          <section className="bg-white dark:bg-gray-800 rounded-xl shadow p-4">
            <h2 className="text-xl font-semibold mb-2">Goals</h2>
            <form onSubmit={handleAddGoal} className="mb-2 flex gap-2">
              <input value={goalTitle} onChange={e => setGoalTitle(e.target.value)} placeholder="New goal title" className="flex-1 px-2 py-1 rounded border" />
              <button type="submit" className="bg-blue-500 text-white px-3 py-1 rounded">Add</button>
            </form>
            <ul className="space-y-1 text-sm">
              {goals.map((g: any) => (
                <li key={g.id} className="border-b last:border-b-0 py-1">{g.title}</li>
              ))}
            </ul>
          </section>
          {/* Tasks */}
          <section className="bg-white dark:bg-gray-800 rounded-xl shadow p-4">
            <h2 className="text-xl font-semibold mb-2">Tasks</h2>
            <form onSubmit={handleAddTask} className="mb-2 flex gap-2">
              <input value={taskTitle} onChange={e => setTaskTitle(e.target.value)} placeholder="New task title" className="flex-1 px-2 py-1 rounded border" />
              <button type="submit" className="bg-blue-500 text-white px-3 py-1 rounded">Add</button>
            </form>
            <ul className="space-y-1 text-sm">
              {tasks.map((t: any) => (
                <li key={t.id} className="border-b last:border-b-0 py-1">{t.title}</li>
              ))}
            </ul>
          </section>
          {/* Check-ins */}
          <section className="bg-white dark:bg-gray-800 rounded-xl shadow p-4">
            <h2 className="text-xl font-semibold mb-2">Check-ins</h2>
            <form onSubmit={handleAddCheckin} className="mb-2 flex gap-2">
              <input value={checkinTaskId} onChange={e => setCheckinTaskId(e.target.value)} placeholder="Task ID" className="w-1/2 px-2 py-1 rounded border" />
              <input value={checkinNotes} onChange={e => setCheckinNotes(e.target.value)} placeholder="Notes" className="flex-1 px-2 py-1 rounded border" />
              <button type="submit" className="bg-blue-500 text-white px-3 py-1 rounded">Add</button>
            </form>
            <ul className="space-y-1 text-sm">
              {checkins.map((c: any) => (
                <li key={c.id} className="border-b last:border-b-0 py-1">Task {c.task_id}: {c.notes}</li>
              ))}
            </ul>
          </section>
        </div>
      </main>
    </div>
  );
}

export default App;
