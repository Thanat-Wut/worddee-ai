
'use client';

import { useState, useEffect } from 'react';
import { api, DashboardStats } from '@/lib/api';

export default function DashboardPage() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const loadStats = async () => {
      try {
        setLoading(true);
        setError('');
        const data = await api.getDashboardStats();
        setStats(data);
      } catch (err) {
        console.error('Error loading stats:', err);
        setError(err instanceof Error ? err.message : 'Failed to load statistics');
      } finally {
        setLoading(false);
      }
    };

    loadStats();
  }, []);

  if (loading) {
    return (
      <div>
        <h2>Your Dashboard</h2>
        <div className="card">
          <div className="loading">Loading statistics</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div>
        <h2>Your Dashboard</h2>
        <div className="error">
          <strong>Error:</strong> {error}
        </div>
      </div>
    );
  }

  if (!stats) {
    return null;
  }

  return (
    <div>
      <h2>Your Dashboard</h2>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-value">{stats.total_sessions}</div>
          <div className="stat-label">Total Sessions</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.average_score.toFixed(1)}</div>
          <div className="stat-label">Average Score</div>
        </div>
        <div className="stat-card">
          <div className="stat-value">{stats.most_common_level || 'N/A'}</div>
          <div className="stat-label">Common Level</div>
        </div>
      </div>

      <div className="card">
        <h3 style={{ marginBottom: '1.5rem', color: '#333' }}>Recent Practice Sessions</h3>
        {stats.recent_sessions.length === 0 ? (
          <p style={{ textAlign: 'center', color: '#999', padding: '2rem' }}>
            No practice sessions yet. Start practicing to see your progress!
          </p>
        ) : (
          <div className="session-list">
            {stats.recent_sessions.map((session) => (
              <div key={session.session_id} className="session-item">
                <div className="session-score">{session.score.toFixed(1)}</div>
                <div className="session-info">
                  <div className="session-sentence">{session.user_sentence}</div>
                  <div className="session-meta">
                    {session.cefr_level} • {new Date(session.practiced_at).toLocaleDateString()}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
