import { useState } from 'react'
import './App.css'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'

function App() {
  const [count, setCount] = useState(0)
  const [activeTab, setActiveTab] = useState('dashboard')

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 p-8">
      {/* Header with logos */}
      <header className="flex justify-center gap-8 mb-8">
        <a href="https://vite.dev" target="_blank" className="transition-transform hover:scale-110">
          <img src={viteLogo} className="h-24" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank" className="transition-transform hover:scale-110">
          <img src={reactLogo} className="h-24 animate-spin-slow" alt="React logo" />
        </a>
      </header>

      {/* Main content */}
      <main className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-center text-blue-600 dark:text-blue-400 mb-8">
          Vite + React + Tailwind CSS
        </h1>

        {/* Card component */}
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 mb-8">
          <div className="flex justify-center mb-4">
            <button
              onClick={() => setCount((count) => count + 1)}
              className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-md transition-colors shadow-md"
            >
              Count is {count}
            </button>
          </div>

          <p className="text-center text-gray-700 dark:text-gray-300">
            Edit <code className="bg-gray-100 dark:bg-gray-700 px-1 rounded">src/App.tsx</code> and save to test HMR
          </p>
        </div>

        {/* Tabs component */}
        <div className="mb-8">
          <div className="flex border-b border-gray-200 dark:border-gray-700">
            {['dashboard', 'team', 'projects', 'calendar'].map((tab) => (
              <button
                key={tab}
                className={`py-2 px-4 capitalize ${activeTab === tab
                    ? 'border-b-2 border-blue-500 font-medium text-blue-600 dark:text-blue-400'
                    : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
                  }`}
                onClick={() => setActiveTab(tab)}
              >
                {tab}
              </button>
            ))}
          </div>
          <div className="p-4 bg-white dark:bg-gray-800 rounded-b-xl shadow-lg">
            <p className="text-gray-600 dark:text-gray-300">
              You've selected: <span className="font-medium text-blue-600 dark:text-blue-400 capitalize">{activeTab}</span>
            </p>
          </div>
        </div>

        {/* Alert component */}
        <div className="bg-green-100 border-l-4 border-green-500 text-green-700 p-4 rounded mb-8" role="alert">
          <div className="flex items-center">
            <svg className="h-5 w-5 mr-2 fill-current" viewBox="0 0 20 20">
              <path d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" />
            </svg>
            <p>Tailwind CSS is working correctly!</p>
          </div>
        </div>

        {/* Documentation link */}
        <p className="text-center text-gray-500 dark:text-gray-400">
          Click on the Vite and React logos to learn more
        </p>
      </main>

      {/* Footer */}
      <footer className="mt-16 text-center text-sm text-gray-500 dark:text-gray-400">
        Built with Tailwind CSS v4.1.4
      </footer>
    </div>
  )
}

export default App
