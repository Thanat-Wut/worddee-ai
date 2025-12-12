/**
 * ════════════════════════════════════════════════════════════════
 * Practice Page (Home)
 * ════════════════════════════════════════════════════════════════
 */
'use client';

import { useState, useEffect } from 'react';
import { api, Word, PracticeResult } from '@/lib/api';
import WordCard from '@/components/WordCard';
import PracticeForm from '@/components/PracticeForm';
import ResultCard from '@/components/ResultCard';

export default function PracticePage() {
  const [word, setWord] = useState<Word | null>(null);
  const [result, setResult] = useState<PracticeResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const loadWord = async () => {
    try {
      setLoading(true);
      setError('');
      setResult(null);
      const data = await api.getRandomWord();
      setWord(data);
    } catch (err) {
      setError('Failed to load word. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (sentence: string) => {
    if (!word) return;

    try {
      setLoading(true);
      setError('');
      const data = await api.submitPractice(word.id, sentence);
      setResult(data);
    } catch (err) {
      setError('Failed to validate sentence. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadWord();
  }, []);

  return (
    <div>
      <h2 style={{ color: 'white', marginBottom: '1rem' }}>Practice Your English</h2>
      
      {error && <div className="error">{error}</div>}
      
      {loading && !word && <div className="loading">Loading word...</div>}
      
      {word && (
        <>
          <WordCard word={word} />
          <PracticeForm onSubmit={handleSubmit} loading={loading} />
          {result && <ResultCard result={result} />}
          <button
            onClick={loadWord}
            style={{
              marginTop: '1rem',
              padding: '0.75rem 1.5rem',
              background: 'white',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontWeight: '600',
            }}
          >
            Next Word →
          </button>
        </>
      )}
    </div>
  );
}
