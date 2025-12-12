/**
 * ════════════════════════════════════════════════════════════════
 * Dashboard Page
 * ════════════════════════════════════════════════════════════════
 */
'use client';

import { useState, useEffect } from 'react';
import { api } from '@/lib/api';

export default function DashboardPage() {
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getDashboardStats()
      .then(setStats)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading">Loading stats...</div>;

  return (
    <div>
      <h2 style={{ color: 'white', marginBottom: '1rem' }}>Your Progress</h2>
      
      <div className="card">
        <h3>Statistics</h3>
        <p><strong>Total Sessions:</strong> {stats?.total_sessions || 0}</p>
        <p><strong>Average Score:</strong> {stats?.average_score || 0}/10</p>
        <p><strong>Most Common Level:</strong> {stats?.most_common_level || 'N/A'}</p>
      </div>

      {stats?.recent_sessions?.length > 0 && (
        <div className="card">
          <h3>Recent Practice</h3>
          {stats.recent_sessions.map((session: any) => (
            <div key={session.session_id} style={{ marginBottom: '1rem', paddingBottom: '1rem', borderBottom: '1px solid #e5e7eb' }}>
              <p><strong>Score:</strong> {session.score}/10</p>
              <p><strong>Sentence:</strong> {session.user_sentence}</p>
              <p style={{ fontSize: '0.875rem', color: '#888' }}>
                {new Date(session.practiced_at).toLocaleString()}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
